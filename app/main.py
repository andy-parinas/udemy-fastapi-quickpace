from fastapi import FastAPI, APIRouter, status
from app.settings import settings
from app.api.v1.api import api_router

app = FastAPI(title="Udemy FastAPI")
root_router = APIRouter()

@root_router.get('/', status_code=status.HTTP_200_OK)
def root() -> dict:
    return {'msg': 'Success'}


app.include_router(root_router)
app.include_router(api_router, prefix=settings.API_V1)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=8000, log_level='debug')
