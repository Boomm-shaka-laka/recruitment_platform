import nb_state_owned_crawler
from db.sqlite_db import RecruitmentDB
import asyncio

sqlite_db = RecruitmentDB("recruitment.db")
def crawler_to_db():
    results = asyncio.run(nb_state_owned_crawler.run())
    sqlite_db.insert_many(results)
    return results

def get_soe_data():
    results = sqlite_db.query_all()
    return results


if __name__ == "__main__":
    crawler_to_db()