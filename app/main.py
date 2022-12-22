from typing import Optional
from fastapi import FastAPI, APIRouter, HTTPException, status

from .schemas import RecipeCreate, Recipe, RecipeSearchResults

RECIPES = [
    {
        "id": 1,
        "label": "Chicken Vesuvio",
        "source": "Serious Eats",
        "url": "http://www.seriouseats.com/recipes/2011/12/chicken-vesuvio-recipe.html",
    },
    {
        "id": 2,
        "label": "Chicken Paprikash",
        "source": "No Recipes",
        "url": "http://norecipes.com/recipe/chicken-paprikash/",
    },
    {
        "id": 3,
        "label": "Cauliflower and Tofu Curry Recipe",
        "source": "Serious Eats",
        "url": "http://www.seriouseats.com/recipes/2011/02/cauliflower-and-tofu-curry-recipe.html",
    },
]

app = FastAPI(title="Udemy FastAPI")
api_router = APIRouter()

@api_router.get('/', status_code=status.HTTP_200_OK)
def root() -> dict:
    return {'msg': 'Success'}


@api_router.get('/recipe/{recipe_id}', status_code=status.HTTP_200_OK)
def fetch_recipe(*, recipe_id: int):
    """
    Fecth as single recipe by ID
    """
    result = [recipe for recipe in RECIPES if recipe['id'] == recipe_id]

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Recipe with id: {recipe_id} not found")


    return result[0]


@api_router.get('/search', status_code=status.HTTP_200_OK, response_model=RecipeSearchResults)
def search_recipes(keyword: Optional[str] = None, max_results: Optional[int] = 10):
    """
    Search for Recipes based on Keyword
    """
    if not keyword:
        return {'results': RECIPES[:max_results]}

    results = filter(lambda recipe: keyword.lower() in recipe['label'].lower(), RECIPES)
    return {'results': list(results)[:max_results]}



@api_router.post('/recipe/', status_code=status.HTTP_201_CREATED, response_model=Recipe)
def create_recipe(*, recipe_in: RecipeCreate):
    """
    Create new Recipe
    """
    new_id = len(RECIPES) + 1
    new_recipe = Recipe(
        id=new_id,
        label=recipe_in.label,
        source=recipe_in.source,
        url=recipe_in.url
    )

    RECIPES.append(new_recipe.dict())

    return new_recipe

app.include_router(api_router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=8000, log_level='debug')
