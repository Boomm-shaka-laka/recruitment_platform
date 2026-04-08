# crawler/bs4_cralwer.py
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
from typing import List, Dict, Optional
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

BASE_URL = "https://gzw.ningbo.gov.cn"
LIST_PAGE_URL = f"{BASE_URL}/col/col1229116730/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"
}

def create_session_with_retries_and_timeout():
    """
    创建一个带有重试策略和连接/读取超时设置的 requests Session 对象。
    这是应对不稳定网络的关键。
    """
    session = requests.Session()
    
    # 定义重试策略
    retry_strategy = Retry(
        total=3,  # 总共重试3次
        status_forcelist=[429, 500, 502, 503, 504],  # 遇到这些状态码就重试
        allowed_methods=["HEAD", "GET", "OPTIONS"],
        backoff_factor=1,  # 重试间隔时间递增
    )
    
    # 创建一个适配器，将重试策略应用上去
    adapter = HTTPAdapter(max_retries=retry_strategy)
    
    # 将适配器挂载到 Session 的 http 和 https 请求上
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    # 更新默认请求头
    session.headers.update(HEADERS)
    
    return session

def extract_source_and_time(text: str) -> tuple[str, str]:
    """从 info 文本中提取来源和发布时间"""
    cleaned = re.sub(r'\s+', ' ', text)
    source_match = re.search(r'来源：\s*([^|]+)', cleaned)
    time_match = re.search(r'发布时间：\s*(\d{4}-\s*\d{2}-\s*\d{2}\s+\d{2}:\s*\d{2})', cleaned)

    source = source_match.group(1).strip() if source_match else ""
    time_str = time_match.group(1).strip() if time_match else ""
    public_time = re.sub(r'\s+', '', time_str)

    if len(public_time) == 15 and public_time[10:11].isdigit():
        fixed_time = public_time[:10] + ' ' + public_time[10:]
    else:
        fixed_time = re.sub(r'^(\d{4}-\d{2}-\d{2})(\d{2}:\d{2})$', r'\1 \2', public_time)

    dt = datetime.strptime(fixed_time, "%Y-%m-%d %H:%M")
    return source, dt

def table_to_markdown(headers: List[str], rows: List[List[str]]) -> str:
    """将表格数据转为 Markdown 表格字符串"""
    if not headers and not rows:
        return ""
    
    max_cols = max(len(headers), *(len(r) for r in rows)) if rows else len(headers)
    headers = list(headers) + [""] * (max_cols - len(headers))
    
    header_line = "| " + " | ".join(str(h) for h in headers) + " |"
    separator = "| " + " | ".join("---" for _ in headers) + " |"
    
    row_lines = []
    for row in rows:
        row = list(row) + [""] * (max_cols - len(row))
        row_line = "| " + " | ".join(str(cell) for cell in row) + " |"
        row_lines.append(row_line)
    
    return "\n".join([header_line, separator] + row_lines)

def parse_zoom_to_markdown(soup: BeautifulSoup) -> str:
    """解析 #zoom 区域，返回 Markdown 格式的正文"""
    zoom = soup.select_one("#zoom")
    if not zoom:
        return ""
    
    parts = []
    
    def walk(element):
        if element.name == 'table':
            rows = []
            for tr in element.select("tr"):
                cells = [td.get_text(strip=True) for td in tr.select("th, td")]
                if any(cells):
                    rows.append(cells)
            if rows:
                headers = rows[0] if len(rows) > 1 else []
                body = rows[1:] if len(rows) > 1 else rows
                md_table = table_to_markdown(headers, body)
                parts.append("\n" + md_table + "\n")
        elif element.name is None:
            text = str(element).strip()
            if text:
                parts.append(text)
        else:
            if element.name not in ('script', 'style'):
                for child in element.children:
                    walk(child)
    
    for child in zoom.children:
        walk(child)
    
    return "\n".join(parts)

def fetch_notice_list() -> List[Dict[str, str]]:
    """
    抓取宁波国资委公告列表
    """
    session = create_session_with_retries_and_timeout()
    try:
        print(f"正在请求列表页: {LIST_PAGE_URL}")
        # 使用 session.get，并设置 (连接超时, 读取超时)
        resp = session.get(LIST_PAGE_URL, timeout=(20, 60))
        resp.raise_for_status()
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, "html.parser")
        
        ul = soup.select_one('#jw_sgzw_二级栏目列表_标题list > div > div > ul')
        if not ul:
            return []
        
        notices = []
        for li in ul.find_all("li"):
            a_tag = li.find("a")
            if a_tag and a_tag.get("href"):
                title = a_tag.get_text(strip=True)
                href = a_tag["href"]
                full_url = urljoin(BASE_URL, href)
                notices.append({"title": title, "url": full_url})
        print(f"成功获取到 {len(notices)} 条公告链接。")
        return notices
    except Exception as e:
        print(f"[ERROR] 获取公告列表失败: {e}")
        return []
    finally:
        session.close()

def fetch_notice_detail(url: str) -> Dict[str, object]:
    """
    抓取单个公告详情
    """
    session = create_session_with_retries_and_timeout()
    try:
        print(f"正在请求详情页: {url}")
        resp = session.get(url, timeout=(20, 60))
        resp.raise_for_status()
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, "html.parser")
        
        info_div = soup.select_one("#right > div:nth-of-type(1)")
        source, public_time = "", ""
        if info_div:
            info_text = info_div.get_text()
            source, public_time = extract_source_and_time(info_text)
        
        summary = parse_zoom_to_markdown(soup)
        print(f"成功获取详情: {url}")
        return {
            "source": source,
            "public_time": public_time,
            "summary": summary
        }
    except Exception as e:
        print(f"[ERROR] 抓取详情页失败 ({url}): {e}")
        return {}
    finally:
        session.close()

# --- 保持原有的 main 函数不变 ---
if __name__ == "__main__":
    results = fetch_notice_list()
    if results:
        result = results[0]
        notice = fetch_notice_detail(result.get("url"))
        print(notice)
    else:
        print("未能获取到任何公告列表。")