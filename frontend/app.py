import streamlit as st
import requests


@st.cache_data
def get_categories() -> list[str]:
    categories = requests.get("http://localhost:8000/catalogue/categories")
    return categories.json()


@st.cache_data
def get_category_items(cat_name: str) -> list[str]:
    cat_items = list()
    if cat_name:
        category_items = requests.get(
            f"http://localhost:8000/catalogue/{cat_name}/items")
        if category_items:
            cat_items = category_items.json()
    return cat_items


curr_category = st.sidebar.selectbox("Item Category",
                                     get_categories(),
                                     index=None)
cat_items = get_category_items(curr_category)

st.sidebar.multiselect("Category Items",
                       [item_info['name'] for item_info in cat_items],
                       default=None)
