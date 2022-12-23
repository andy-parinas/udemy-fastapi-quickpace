from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import schemas
from app import repositories as repo
from app.db.session import get_db
from app.services import auth
router = APIRouter()

@router.post('signup', response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def register_user(*, user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    user = repo.user.get_by_email(db=db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exist"
        )
    user = repo.user.create(db=db, obj_in=user_in)

    return user

@router.post('/login')
def login( db: Session = Depends(get_db),  form_data: OAuth2PasswordRequestForm = Depends()):

    user = auth.authenticate(email=form_data.username, password=form_data.password, db=db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "Invalid username or password"
        )

    return {
        "access_token": auth.create_access_token(sub=user.id),
        "token_type": "bearer"
    }
