import sqlite3
import logging
from datetime import datetime
from typing import Optional
from contextlib import contextmanager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class RecruitmentDB:
    """
    SQLite 数据库管理类
    管理招聘信息表 recruitment_info_soe 的增删查操作
    """

    TABLE_NAME = "recruitment_info_soe"

    def __init__(self, db_path: str = "recruitment.db"):
        """
        初始化数据库连接

        :param db_path: 数据库文件路径，默认为 recruitment.db
        """
        self.db_path = db_path
        self._check_connection()
        self.create_table()

    # ─────────────────────────────────────────────
    # 连接检查
    # ─────────────────────────────────────────────

    def _check_connection(self):
        """检查数据库是否可正常连接"""
        try:
            with self._get_connection() as conn:
                conn.execute("SELECT 1")
            logger.info(f"✅ 数据库连接正常：{self.db_path}")
        except sqlite3.Error as e:
            logger.error(f"❌ 数据库连接失败：{e}")
            raise ConnectionError(f"无法连接到数据库 {self.db_path}：{e}")

    @contextmanager
    def _get_connection(self):
        """
        上下文管理器：安全获取数据库连接，用完自动关闭
        使用 WAL 模式提升并发读写性能
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row          # 查询结果可按列名访问
        conn.execute("PRAGMA journal_mode=WAL") # 写前日志，提升性能
        conn.execute("PRAGMA foreign_keys=ON")  # 启用外键约束
        try:
            yield conn
            conn.commit()
        except sqlite3.Error as e:
            conn.rollback()
            logger.error(f"数据库操作失败，已回滚：{e}")
            raise
        finally:
            conn.close()

    # ─────────────────────────────────────────────
    # 建表
    # ─────────────────────────────────────────────

    def create_table(self):
        ddl = f"""
        CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            title               TEXT    NOT NULL UNIQUE,  -- ←←← 关键：加上 UNIQUE
            public_time         TEXT,
            insert_time         TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
            click_through_rate  REAL,
            href                TEXT,
            source              TEXT,
            summary             TEXT,
            enrollment_time     TEXT,
            end_time            TEXT
        );
        """
        with self._get_connection() as conn:
            conn.execute(ddl)
        logger.info(f"✅ 表 [{self.TABLE_NAME}] 已就绪")
    # ─────────────────────────────────────────────
    # 插入数据
    # ─────────────────────────────────────────────

    def insert(
        self,
        title: str,
        public_time: Optional[str] = None,
        click_through_rate: Optional[float] = None,
        href: Optional[str] = None,  # ← 注意：你漏了这个参数！
        source: Optional[str] = None,
        summary: Optional[str] = None,
        enrollment_time: Optional[str] = None,
        end_time: Optional[str] = None,
    ) -> int:
        if not title or not title.strip():
            raise ValueError("title 不能为空")

        insert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        sql = f"""
        INSERT OR IGNORE INTO {self.TABLE_NAME}
            (title, public_time, insert_time, click_through_rate,
            source, summary, enrollment_time, end_time, href)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """  # ← 注意：你原来漏了 href 字段！
        
        params = (
            title.strip(),
            public_time,
            insert_time,
            click_through_rate,
            source,
            summary,
            enrollment_time,
            end_time,
            href,  # ← 补上
        )

        with self._get_connection() as conn:
            cursor = conn.execute(sql, params)
            new_id = cursor.lastrowid

        if new_id == 0:
            logger.info(f"⚠️ 插入跳过（title 已存在）：'{title}'")
            return 0  # 或者返回 -1 表示未插入
        else:
            logger.info(f"✅ 插入成功，id={new_id}，title='{title}'")
            return new_id

    def insert_many(self, records: list[dict]) -> int:
        if not records:
            logger.warning("insert_many：传入数据为空，跳过")
            return 0

        insert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = f"""
        INSERT OR IGNORE INTO {self.TABLE_NAME}
            (title, public_time, insert_time, click_through_rate,
            source, summary, enrollment_time, end_time, href)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params_list = []
        for rec in records:
            title = rec.get("title", "").strip()
            params_list.append((
                title,
                rec.get("public_time"),
                insert_time,
                rec.get("click_through_rate", 0),
                rec.get("source"),
                rec.get("summary", ""),
                rec.get("enrollment_time"),
                rec.get("end_time"),
                rec.get("href")
            ))

        with self._get_connection() as conn:
            cursor = conn.executemany(sql, params_list)
            actual_count = conn.total_changes  # 获取实际插入行数

        print(f"✅ 批量插入完成，尝试 {len(params_list)} 条，实际新增 {actual_count} 条")
        logger.info(f"✅ 批量插入完成，尝试 {len(params_list)} 条，实际新增 {actual_count} 条")
        return actual_count


    # ─────────────────────────────────────────────
    # 辅助查询（方便调试验证）
    # ─────────────────────────────────────────────

    def query_all(self) -> list[dict]:
        """查询全部记录，返回字典列表"""
        sql = f"SELECT * FROM {self.TABLE_NAME} ORDER BY id"
        with self._get_connection() as conn:
            rows = conn.execute(sql).fetchall()
        return [dict(row) for row in rows]

    def count(self) -> int:
        """返回当前表记录总数"""
        sql = f"SELECT COUNT(*) FROM {self.TABLE_NAME}"
        with self._get_connection() as conn:
            result = conn.execute(sql).fetchone()
        return result[0]


# ─────────────────────────────────────────────────
# 使用示例
# ─────────────────────────────────────────────────

if __name__ == "__main__":
    db = RecruitmentDB("recruitment.db")
    db.create_table()

    # # 单条插入
    # db.insert(
    #     title="2025年国有企业招聘公告",
    #     public_time="2025-03-01",
    #     click_through_rate=0.42,
    #     source="国资委官网",
    #     summary="面向应届毕业生招聘若干名",
    #     enrollment_time="2025-03-10",
    #     end_time="2025-04-10",
    # )

    # 批量插入
    # db.insert_many([
    #     {
    #         "title": "央企2025春季招聘",
    #         "source": "央企招聘网",
    #         "public_time": "2025-02-20",
    #         "end_time": "2025-03-31",
    #     },
    #     {
    #         "title": "地方国企人才引进计划",
    #         "source": "地方国资委",
    #         "click_through_rate": 0.28,
    #         "end_time": "2025-05-01",
    #     },
    # ])

    print(f"当前记录数：{db.count()}")
    print("所有记录：")
    for row in db.query_all():
        print(row)

    print(f"删除后记录数：{db.count()}")