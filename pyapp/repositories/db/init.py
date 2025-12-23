"""
数据库orm连接
"""
import os
import json
import logging
from contextlib import contextmanager
from typing import Any, Optional

from sqlalchemy import create_engine, types
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import Dialect

from config import DATA_DIR, DATABASE_HOST, DATABASE_NAME, DATABASE_PASSWORD, DATABASE_USER, DB_TYPE

log = logging.getLogger(__name__)

class JSONField(types.TypeDecorator):
    impl = types.Text
    cache_ok = True

    def process_bind_param(self, value: Optional[Any], dialect: Dialect) -> Any:
        if value is None:
            return None
        return json.dumps(value, ensure_ascii=False)

    def process_result_value(self, value: Optional[Any], dialect: Dialect) -> Any:
        if value is not None:
            return json.loads(value)

if DB_TYPE == "mysql":
    # 数据库连接初始化
    username = DATABASE_USER
    password = DATABASE_PASSWORD
    host=f"{DATABASE_HOST}:3306"
    database= DATABASE_NAME
    print(f"使用mysql作为数据库,User: {DATABASE_USER}, HOST: {host}")
    
    DATABASE_URL = f"mysql+pymysql://{username}:{password}@{host}/{database}"
else:
    print("使用sqlite作为数据库")
    DATABASE_URL = os.getenv("SQLITE_URL", f"sqlite:///{str(DATA_DIR)}/test.db")


engine = create_engine(
        DATABASE_URL, 
        pool_pre_ping=True,
        pool_recycle=3600,
        json_serializer=lambda obj: json.dumps(obj,ensure_ascii=False),
        )

SessionLocal = sessionmaker(
        autoflush=False, 
        bind=engine, 
        expire_on_commit=False
        )

Base = declarative_base()

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

get_db = contextmanager(get_session)
