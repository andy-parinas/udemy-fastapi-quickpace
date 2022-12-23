from typing import Optional
from sqlalchemy.orm import Session

from app.repositories.base import RepositoryBase
from app.models.user import User
from app.schemas.user import  UserCreate, UserUpdate
from app.services.security import get_password_hash


class UserRepository(RepositoryBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()


    def is_userpuser(self, user: User) -> bool:
        return user.is_superuser

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        create_data = obj_in.dict()
        create_data.pop("password")
        db_obj = User(**create_data)
        db_obj.hashed_password = get_password_hash(obj_in.password)
        db.add(db_obj)
        db.commit()

        return db_obj

user = UserRepository(User)