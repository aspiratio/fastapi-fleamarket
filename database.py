from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import get_settings


SQLALCHEMY_DATABASE_URL = get_settings().sqlalchemy_database_url  # DBへの接続情報


engine = create_engine(SQLALCHEMY_DATABASE_URL)  # DBへの接続を保持したエンジン

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)  # DBに対する操作をひとまとめにしてDBに適用するためのセッション

Base = declarative_base()  # DBモデルを作成するためのベースとなるクラス


def get_db():
    db = SessionLocal()
    try:
        yield db  # yieldを使用するとFastAPIがレスポンスを返した後に後続処理を行える → finallyのclose()を確実に実行させる
    finally:
        db.close()
