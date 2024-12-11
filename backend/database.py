# backend/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./hotel.db"  # 使用SQLite数据库，生产环境建议使用PostgreSQL等

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}  # SQLite特有参数
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
