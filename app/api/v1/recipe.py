from typing import Optional, List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app import repositories as repo
from app.db.session import get_db
from app.schemas.recipe import RecipeSearchResults, RecipeCreate, Recipe



router = APIRouter()


@router.get('/{recipe_id}', status_code=status.HTTP_200_OK)
def fetch_recipe(*, recipe_id: int, db:Session = Depends(get_db)):
    """
    Fecth as single recipe by ID
    """
    result = repo.recipe.get(db=db, id=recipe_id)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Recipe with id: {recipe_id} not found")

    return result


@router.get('/search', status_code=status.HTTP_200_OK, response_model=RecipeSearchResults)
def search_recipes(
        keyword: Optional[str] = None,
        max_results: Optional[int] = 10,
        db: Session = Depends(get_db)
):
    """
    Search for Recipes based on Keyword
    """
    if not keyword:
        return {'results': repo.recipe.getMany(db=db, limit=max_results)}

    results = repo.recipe.search_keyword(db=db, keyword=keyword, limit=max_results)
    return {'results': list(results)}



@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Recipe)
def create_recipe(*, recipe_in: RecipeCreate, db: Session = Depends(get_db)):
    """
    Create new Recipe
    """
    recipe = repo.recipe.create(db=db, obj_in=recipe_in)
    return recipe