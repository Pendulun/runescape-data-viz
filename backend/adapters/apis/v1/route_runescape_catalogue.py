from adapters.server import ServerAdapters

from fastapi import APIRouter

router = APIRouter()


@router.get("/{category_name}")
def category_info(category_name: str):
    return ServerAdapters.category_service.get_category_info(category_name)


@router.get("/{category_name}/items")
def category_items(category_name: str):
    return ServerAdapters.category_service.get_category_items(category_name)

@router.get("/item/{item_id}")
def item_info(item_id:int):
    return ServerAdapters.item_service.get_item_info(item_id)

@router.get("/item/{item_id}/prices")
def item_prices(item_id:int):
    return ServerAdapters.item_service.get_item_prices(item_id)
