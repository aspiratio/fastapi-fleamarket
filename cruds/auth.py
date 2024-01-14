from sqlalchemy.orm import Session
from schemas import UserCreate
from models import User


def create_user(db: Session, user_create: UserCreate):
    new_user = User(**user_create.model_dump())  # Userモデルを作成
    db.add(new_user)
    db.commit()

    return new_user
