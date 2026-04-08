from crawler.bs4_cralwer import fetch_notice_list, fetch_notice_detail
from db.sqlite_db import RecruitmentDB

sqlite_db = RecruitmentDB("recruitment.db")
def crawler_to_db():
    notice_list = fetch_notice_list()
    print(notice_list)
    results = []
    for notice in notice_list:
        title = notice.get("title")
        href = notice.get("url")
        result = fetch_notice_detail(notice['url'])
        result["title"] = title
        result["href"] = href
        results.append(result)
    sqlite_db.insert_many(results)
    return results

def get_soe_data():
    results = sqlite_db.query_all()
    return results



if __name__ == "__main__":
    crawler_to_db()