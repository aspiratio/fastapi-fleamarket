from datetime import datetime, timedelta
import hashlib
import base64
import os
from jose import jwt
from sqlalchemy.orm import Session
from schemas import UserCreate
from models import User


ALGORITHM = "HS256"
SECRET_KEY = "54131ea955abdf2a9bd1d3ece93eec3434220e3da92944f1b7127663061b1496"


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


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    expires = datetime.now() + expires_delta
    payload = {"sub": username, "id": user_id, "exp": expires}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
