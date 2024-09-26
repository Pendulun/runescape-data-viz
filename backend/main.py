from apis.base import api_router
from core.config import settings

from fastapi import FastAPI

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}