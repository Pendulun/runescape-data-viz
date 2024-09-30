from adapters.server import ServerAdapters

from fastapi import APIRouter

router = APIRouter()


@router.get("/{category_name}")
def category_info(category_name: str):
    return ServerAdapters.category_service.get_category_info(category_name)


@router.get("/{category_name}/items")
def category_items(category_name: str):
    return ServerAdapters.category_service.get_category_items(category_name)
