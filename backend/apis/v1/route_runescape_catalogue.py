from repository.items_categories import get_category_id

from fastapi import APIRouter
import requests
from core.config import runescapeRoutesFormats

router = APIRouter()


@router.get("/catalogue/{category_name}")
def catalogue(category_name: str):
    cat_id = get_category_id(category_name.lower())
    if cat_id:
        request_url = runescapeRoutesFormats.CATEGORY.format(cat_id)
        category_info = requests.get(request_url)
        data = category_info.json()
        return data
    else:
        return None
