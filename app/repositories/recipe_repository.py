from typing import List
from sqlalchemy.orm import Session
from app.repositories.base import RepositoryBase
from app.models.recipe import Recipe
from app.schemas.recipe import RecipeCreate, RecipeUpdate


class RecipeRepository(RepositoryBase[Recipe, RecipeCreate, RecipeUpdate]):
    def search_keyword(self, db: Session, *, keyword: str, limit: int = 0) -> List[Recipe]:
        return db.query(Recipe)\
            .filter(Recipe.label.ilike(f"%{keyword}%"))\
            .limit(limit).all()

recipe = RecipeRepository(Recipe)
