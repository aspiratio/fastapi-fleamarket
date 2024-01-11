from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


SQLALCHEMY_DATABASE_URL = (
    "postgresql://fastapiuser:fastapipass@0.0.0.0:5432/fleamarket"  # DBへの接続情報
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)  # DBへの接続を保持したエンジン

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)  # DBに対する操作をひとまとめにしてDBに適用するためのセッション

Base = declarative_base()  # DBモデルを作成するためのベースとなるクラス