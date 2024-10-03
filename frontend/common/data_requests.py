import streamlit as st
import requests

@st.cache_data
def get_categories() -> list[str]:
    response = requests.get("http://localhost:8000/catalogue/categories")
    categories = response.json()
    categories = sorted(categories)
    return categories


@st.cache_data
def get_category_items(cat_name: str) -> list[str]:
    cat_items = list()
    if cat_name:
        category_items = requests.get(
            f"http://localhost:8000/catalogue/{cat_name}/items")
        if category_items:
            cat_items = category_items.json()
    return cat_items


@st.cache_data
def get_item_info(item_id: int) -> dict | None:
    if item_id is not None:
        response = requests.get(
            f"http://localhost:8000/catalogue/item/{item_id}")
        if response:
            return response.json()
    return None

@st.cache_data
def get_item_historical_prices(item_id: int) -> dict | None:
    if item_id is not None:
        response = requests.get(
            f"http://localhost:8000/catalogue/item/{item_id}/prices"
        )
        if response:
            return response.json()
    return None