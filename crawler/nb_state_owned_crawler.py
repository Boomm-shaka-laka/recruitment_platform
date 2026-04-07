import asyncio
import re
import logging
from playwright.async_api import async_playwright


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

BASE_URL = "https://gzw.ningbo.gov.cn"
TARGET_URL = f"{BASE_URL}/col/col1229116730/"
LIST_XPATH = '/html/body/div/div[3]/div/div/div[2]/div/div/div/ul'


# ─────────────────────────────────────────────
# ✅ 列表页：只拦图片
# ─────────────────────────────────────────────
async def route_list(route):
    if route.request.resource_type == "image":
        await route.abort()
    else:
        await route.continue_()


# ─────────────────────────────────────────────
# ✅ 详情页：激进拦截
# ─────────────────────────────────────────────
async def route_detail(route):
    if route.request.resource_type in ["image", "stylesheet", "font"]:
        await route.abort()
    else:
        await route.continue_()


# ─────────────────────────────────────────────
# HTML 表格 → Markdown
# ─────────────────────────────────────────────
def table_element_to_markdown(headers, rows):
    if not headers and not rows:
        return ""

    if not headers and rows:
        headers = [""] * len(rows[0])

    def esc(x):
        return str(x).replace("|", "\\|").replace("\n", " ").strip()

    header = "| " + " | ".join(esc(h) for h in headers) + " |"
    sep = "| " + " | ".join("---" for _ in headers) + " |"
    body = ["| " + " | ".join(esc(c) for c in r) + " |" for r in rows]

    return "\n".join([header, sep] + body)


# ─────────────────────────────────────────────
# 解析正文
# ─────────────────────────────────────────────
async def parse_zoom_to_markdown(page):
    zoom = await page.query_selector("#zoom")
    if not zoom:
        return ""

    node_data = await page.evaluate("""
    () => {
        const zoom = document.getElementById('zoom');
        if (!zoom) return [];

        const res = [];

        function walk(node){
            if(node.nodeType===Node.TEXT_NODE){
                const t=node.textContent.trim();
                if(t) res.push({type:'text',content:t});
                return;
            }
            if(node.nodeType!==Node.ELEMENT_NODE) return;

            if(node.tagName.toLowerCase()==='table'){
                const rows=[...node.querySelectorAll('tr')].map(tr =>
                    [...tr.querySelectorAll('th,td')].map(td=>td.innerText.trim())
                );
                res.push({type:'table',headers:rows[0]||[],rows:rows.slice(1)});
                return;
            }

            [...node.childNodes].forEach(walk);
        }

        [...zoom.childNodes].forEach(walk);
        return res;
    }
    """)

    parts = []
    for n in node_data:
        if n["type"] == "text":
            parts.append(n["content"])
        else:
            parts.append("\n" + table_element_to_markdown(n["headers"], n["rows"]) + "\n")
    
    return "\n".join(parts)


# ─────────────────────────────────────────────
# 提取来源+时间
# ─────────────────────────────────────────────
def extract_source_and_time(text):
    source = re.search(r'来源[：:]\s*([^|]+)', text)
    time = re.search(r'发布时间[：:]\s*([\d\s\-:]+)', text)

    source = source.group(1).strip() if source else ""
    time = re.sub(r"\s+", "", time.group(1)) if time else ""

    return source, time


# ─────────────────────────────────────────────
# 🚀 抓列表
# ─────────────────────────────────────────────
async def scrape_list(context):
    page = await context.new_page()

    # ✅ 只拦图片
    await page.route("**/*", lambda r: asyncio.create_task(route_list(r)))

    logger.info("抓列表页（只拦图片）")
    await page.goto(TARGET_URL, wait_until="commit", timeout=90_000)

    await page.wait_for_selector(f'xpath={LIST_XPATH}')

    items = []
    lis = await page.query_selector_all(f'xpath={LIST_XPATH}/li')

    for li in lis:
        a = await li.query_selector("a")
        p = await li.query_selector("p")

        if not a:
            continue

        href = await a.get_attribute("href") or ""
        title = (await a.inner_text()).strip()
        time = (await p.inner_text()).strip() if p else ""

        if href.startswith("/"):
            href = BASE_URL + href

        items.append({
            "href": href,
            "title": title,
            "public_time": time
        })

    await page.close()
    return items


# ─────────────────────────────────────────────
# 🚀 并发抓详情
# ─────────────────────────────────────────────
async def scrape_detail(context, items, concurrency=3):
    sem = asyncio.Semaphore(concurrency)

    async def worker(item):
        async with sem:
            page = await context.new_page()

            # ✅ 详情页激进拦截
            await page.route("**/*", lambda r: asyncio.create_task(route_detail(r)))

            try:
                await page.goto(item["href"], wait_until="commit", timeout=90_000) # domcontentloaded很慢

                info = await page.query_selector('xpath=//*[@id="right"]/div[1]')
                if info:
                    txt = await info.inner_text()
                    source, public_time = extract_source_and_time(txt)
                    item["source"] = source
                    item["public_time"] = public_time

                locator = page.locator("#artcount")

                # await locator.wait_for()
                # await page.wait_for_function(
                #     "document.querySelector('#artcount')?.innerText.trim() !== ''"
                # )

                # num = await locator.inner_text()
                # item["click_through_rate"] = int(re.sub(r"\D", "", num) or 0)

                item["summary"] = await parse_zoom_to_markdown(page)

            except Exception as e:
                logger.error(f"失败: {item['href']} | {e}")

            finally:
                await page.close()

    await asyncio.gather(*(worker(i) for i in items))
    return items


# ─────────────────────────────────────────────
# 🚀 主程序
# ─────────────────────────────────────────────
async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
        context = await browser.new_context(
            locale="zh-CN",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            )


        items = await scrape_list(context)
        items = await scrape_detail(context, items, concurrency=3)

        await browser.close()

        return items

        # print("\n" + "=" * 50)
        # for i in items[:5]:
        #     print(i["title"])
        #     print(i.get("source"))
        #     print(i.get("public_time"))
        #     print(i.get("click_through_rate"))
        #     print((i.get("content") or "")[:100])
        #     print("-" * 30)


if __name__ == "__main__":
    results = asyncio.run(run())
    print(results)