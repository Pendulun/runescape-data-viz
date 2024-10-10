from datetime import datetime
import streamlit as st

from backend.domain.categoryServiceImp import CategoryServiceImp
from backend.domain.itemServiceImp import ItemServiceImp
from backend.domain.runescapeAPIServiceImp import RunescapeAPIInfo
from backend.adapters.categoryRepoImp import CategoryRepoRequest
from backend.adapters.itemRepoImp import ItemRepoRequest
from backend.adapters.runescapeAPIRepoImp import RunescapeAPIInfoRepo


def get_last_updated() -> datetime:
    last_updated = RunescapeAPIInfo(RunescapeAPIInfoRepo()).get_last_updated()
    return last_updated

@st.cache_data
def get_categories() -> list[str]:
    categories = CategoryServiceImp(CategoryRepoRequest()).get_categories()
    return categories


@st.cache_data(hash_funcs={datetime: lambda dt: dt.isoformat()})
def get_category_items(cat_name: str, today: datetime) -> list[str]:
    cat_items = CategoryServiceImp(
        CategoryRepoRequest()).get_category_items(cat_name)
    if not cat_items:
        cat_items = list()
    return cat_items


@st.cache_data
def get_item_info(item_id: int) -> dict | None:
    item_info = ItemServiceImp(ItemRepoRequest()).get_item_info(item_id)
    return item_info


@st.cache_data(hash_funcs={datetime: lambda dt: dt.isoformat()})
def get_item_historical_prices(item_id: int, today: datetime) -> dict | None:
    item_prices = ItemServiceImp(ItemRepoRequest()).get_item_prices(item_id)
    return item_prices
