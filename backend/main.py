from apis.base import api_router
from core.config import Settings

from fastapi import FastAPI

app = FastAPI(title=Settings.PROJECT_NAME, version=Settings.PROJECT_VERSION)
app.include_router(api_router)