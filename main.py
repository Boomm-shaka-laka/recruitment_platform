# main.py
from fastapi import FastAPI
import uvicorn
import logging
from crawler.bs4_cralwer import fetch_notice_list, fetch_notice_detail
from db.sqlite_db import RecruitmentDB

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello! The crawler service is running. Call /run-crawler to start the job."}

@app.get("/run-crawler")
def run_crawler():
    """
    一个Web钩子，当被调用时，会执行完整的爬取和存储流程。
    """
    try:
        logger.info("接收到爬取任务请求，开始执行...")
        notice_list = fetch_notice_list()
        if not notice_list:
            logger.warning("未能获取到任何公告列表。")
            return {"status": "warning", "message": "No notices found.", "count": 0}

        results = []
        for notice in notice_list:
            title = notice.get("title")
            href = notice.get("url")
            result = fetch_notice_detail(notice['url'])
            result["title"] = title
            result["href"] = href
            results.append(result)
        
        return {"status": "success", "message": f"Crawling task completed. Processed {len(results)} items.", "count": len(results), "data": results}
    
    except Exception as e:
        error_msg = f"爬取任务执行失败: {e}"
        logger.error(error_msg)
        return {"status": "error", "message": error_msg}


if __name__ == "__main__":
    # 为了让它能在本地测试
    uvicorn.run(app, host="0.0.0.0", port=8000)