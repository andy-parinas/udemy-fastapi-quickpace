from typing import Optional

from app.repositories.base import RepositoryBase
from app.models.user import User
from app.schemas.user import  UserCreate, UserUpdate
from sqlalchemy.orm import Session

class UserRepository(RepositoryBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()


    def is_userpuser(self, user: User) -> bool:
        return user.is_superuser


user = UserRepository(User)