import streamlit as st
import requests

from common import data_requests_only

@st.cache_data
def get_categories() -> list[str]:
    return data_requests_only.get_categories()


@st.cache_data
def get_category_items(cat_name: str) -> list[str]:
    return data_requests_only.get_category_items(cat_name)


@st.cache_data
def get_item_info(item_id: int) -> dict | None:
    return data_requests_only.get_item_info(item_id)

@st.cache_data
def get_item_historical_prices(item_id: int) -> dict | None:
    return data_requests_only.get_item_historical_prices(item_id)