import hashlib
import base64
import os
from sqlalchemy.orm import Session
from schemas import UserCreate
from models import User


def create_user(db: Session, user_create: UserCreate):
    salt = base64.b64encode(os.urandom(32))  # ランダムな文字列
    hashed_password = hashlib.pbkdf2_hmac(
        "sha256", user_create.password.encode(), salt, 1000
    ).hex()  # パスワードにソルトを付け足した上でハッシュ化する

    new_user = User(
        username=user_create.username,
        password=hashed_password,
        salt=salt.decode(),
    )  # Userモデルを作成
    db.add(new_user)
    db.commit()

    return new_user


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    hashed_password = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), user.salt.encode(), 1000
    ).hex()
    if user.password != hashed_password:
        return None

    return user
