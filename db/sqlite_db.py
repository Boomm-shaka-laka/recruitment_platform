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
        """
        创建招聘信息表 recruitment_info_soe（若已存在则跳过）

        字段说明：
          id                INTEGER  主键，自增
          title             TEXT     招聘标题（必填）
          public_time       TEXT     发布时间
          insert_time       TEXT     入库时间（自动填充）
          click_through_rate REAL    点击率
          href              TEXT     链接
          source            TEXT     数据来源
          summary           TEXT     摘要
          enrollment_time   TEXT     报名开始时间
          end_time          TEXT     报名截止时间
        """
        ddl = f"""
        CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            title               TEXT    NOT NULL,
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
        source: Optional[str] = None,
        summary: Optional[str] = None,
        enrollment_time: Optional[str] = None,
        end_time: Optional[str] = None,
    ) -> int:
        """
        插入单条招聘记录

        :param title:               招聘标题（必填）
        :param public_time:         发布时间，格式建议 'YYYY-MM-DD'
        :param click_through_rate:  点击率，如 0.35 表示 35%
        :param source:              数据来源，如 '国资委官网'
        :param href:                链接
        :param summary:             招聘摘要
        :param enrollment_time:     报名开始时间
        :param end_time:            报名截止时间
        :return:                    新插入记录的 id
        """
        if not title or not title.strip():
            raise ValueError("title 不能为空")

        insert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        sql = f"""
        INSERT INTO {self.TABLE_NAME}
            (title, public_time, insert_time, click_through_rate,
             source, summary, enrollment_time, end_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            title.strip(),
            public_time,
            insert_time,
            click_through_rate,
            source,
            summary,
            enrollment_time,
            end_time,
        )

        with self._get_connection() as conn:
            cursor = conn.execute(sql, params)
            new_id = cursor.lastrowid

        logger.info(f"✅ 插入成功，id={new_id}，title='{title}'")
        return new_id

    def insert_many(self, records: list[dict]) -> int:
        """
        批量插入招聘记录

        :param records: 字典列表，每个字典的 key 对应字段名，title 为必填
        :return:        成功插入的条数
        """
        if not records:
            logger.warning("insert_many：传入数据为空，跳过")
            return 0

        insert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = f"""
        INSERT INTO {self.TABLE_NAME}
            (title, public_time, insert_time, click_through_rate,
             source, summary, enrollment_time, end_time,href)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params_list = []
        for rec in records:
            if not rec.get("title", "").strip():
                raise ValueError(f"批量插入中存在空 title，记录：{rec}")
            params_list.append((
                rec["title"].strip(),
                rec.get("public_time"),
                insert_time,
                rec.get("click_through_rate"),
                rec.get("source"),
                rec.get("summary"),
                rec.get("enrollment_time"),
                rec.get("end_time"),
                rec.get("href")
            ))

        with self._get_connection() as conn:
            conn.executemany(sql, params_list)

        count = len(params_list)
        print(f"✅ 批量插入成功，共 {count} 条")
        logger.info(f"✅ 批量插入成功，共 {count} 条")
        return count

    # ─────────────────────────────────────────────
    # 删除数据
    # ─────────────────────────────────────────────

    def delete_by_id(self, record_id: int) -> bool:
        """
        按主键删除单条记录

        :param record_id: 记录 id
        :return:          True=删除成功，False=记录不存在
        """
        sql = f"DELETE FROM {self.TABLE_NAME} WHERE id = ?"
        with self._get_connection() as conn:
            cursor = conn.execute(sql, (record_id,))
            affected = cursor.rowcount

        if affected:
            logger.info(f"✅ 删除成功，id={record_id}")
            return True
        else:
            logger.warning(f"⚠️ 未找到 id={record_id} 的记录")
            return False

    def delete_by_condition(
        self,
        source: Optional[str] = None,
        end_time_before: Optional[str] = None,
        title_keyword: Optional[str] = None,
    ) -> int:
        """
        按条件删除记录（多条件取交集）

        :param source:          按来源精确匹配删除
        :param end_time_before: 删除截止时间早于此值的记录，格式 'YYYY-MM-DD'
        :param title_keyword:   按标题关键词模糊删除
        :return:                实际删除的条数
        """
        conditions = []
        params = []

        if source:
            conditions.append("source = ?")
            params.append(source)
        if end_time_before:
            conditions.append("end_time < ?")
            params.append(end_time_before)
        if title_keyword:
            conditions.append("title LIKE ?")
            params.append(f"%{title_keyword}%")

        if not conditions:
            raise ValueError("至少需要指定一个删除条件，避免误删全表")

        sql = f"DELETE FROM {self.TABLE_NAME} WHERE {' AND '.join(conditions)}"

        with self._get_connection() as conn:
            cursor = conn.execute(sql, params)
            affected = cursor.rowcount

        logger.info(f"✅ 条件删除完成，共删除 {affected} 条")
        return affected

    def delete_all(self) -> int:
        """
        清空整张表（谨慎使用！）

        :return: 删除的条数
        """
        sql = f"DELETE FROM {self.TABLE_NAME}"
        with self._get_connection() as conn:
            cursor = conn.execute(sql)
            affected = cursor.rowcount
        logger.warning(f"⚠️ 已清空表 [{self.TABLE_NAME}]，共删除 {affected} 条")
        return affected

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

    # 按 id 删除
    db.delete_by_id(1)

    # 按条件删除（截止时间早于 2025-04-01 且来源为央企招聘网）
    db.delete_by_condition(source="央企招聘网", end_time_before="2025-04-01")

    print(f"删除后记录数：{db.count()}")