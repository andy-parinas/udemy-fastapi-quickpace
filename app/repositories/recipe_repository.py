from app.repositories.base import RepositoryBase
from app.models.recipe import Recipe
from app.schemas.recipe import RecipeCreate, RecipeUpdate


class RecipeRepository(RepositoryBase[Recipe, RecipeCreate, RecipeUpdate]):
    ...


recipe = RecipeRepository(Recipe)
