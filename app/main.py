from typing import Optional
from fastapi import FastAPI, APIRouter, status


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
    if result:
        return result[0]


@api_router.get('/search', status_code=status.HTTP_200_OK)
def search_recipes(keyword: Optional[str] = None, max_results: Optional[int] = 10):
    """
    Search for Recipes based on Keyword
    """
    if not keyword:
        return {'results': RECIPES[:max_results]}

    results = filter(lambda recipe: keyword.lower() in recipe['label'].lower(), RECIPES)
    return {'results': list(results)[:max_results]}

app.include_router(api_router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=8000, log_level='debug')
