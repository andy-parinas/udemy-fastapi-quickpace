from fastapi import APIRouter

from app.api.v1 import recipe

api_router = APIRouter()
api_router.include_router(recipe.router, prefix='/recipe', tags=['Recipe'])