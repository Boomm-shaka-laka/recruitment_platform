import asyncio
from nb_state_owned_crawler import run  # 你的爬虫函数
from db.sqlite_db import RecruitmentDB # 你的数据库操作类

async def main():
    db = RecruitmentDB("recruitment.db")
    print("🚀 开始抓取数据...")
    results = await run()
    if results:
        db.insert_many(results)
        print(f"✅ 成功更新 {len(results)} 条数据")
    else:
        print("⚠️ 未发现新数据")

if __name__ == "__main__":
    asyncio.run(main())