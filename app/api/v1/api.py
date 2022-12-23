from fastapi import APIRouter

from app.api.v1 import recipe
from app.api.v1 import auth

api_router = APIRouter()
api_router.include_router(recipe.router, prefix='/recipe', tags=['Recipe'])
api_router.include_router(auth.router, prefix='/auth', tags=['Auth'])