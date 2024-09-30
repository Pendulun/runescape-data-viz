from adapters.apis.base import api_router
from adapters.server import ServerAdapters
from adapters.categoryRepoImp import CategoryRepoRequest
from domain.categoryServiceImp import CategoryServiceImp
from adapters.itemRepoImp import ItemRepoRequest
from domain.itemServiceImp import ItemServiceImp
from core.config import Settings

from fastapi import FastAPI

ServerAdapters.category_service = CategoryServiceImp(CategoryRepoRequest())
ServerAdapters.item_service = ItemServiceImp(ItemRepoRequest())

app = FastAPI(title=Settings.PROJECT_NAME, version=Settings.PROJECT_VERSION)
app.include_router(api_router)