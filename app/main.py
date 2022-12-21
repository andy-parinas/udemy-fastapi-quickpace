from fastapi import FastAPI, APIRouter, status

app = FastAPI(title="Udemy FastAPI")

api_router = APIRouter()

@api_router.get('/', status_code=status.HTTP_200_OK)
def root() -> dict:
    return {'msg': 'Success'}


app.include_router(api_router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=8000, log_level='debug')
