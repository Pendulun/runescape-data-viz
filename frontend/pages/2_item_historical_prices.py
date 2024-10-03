import streamlit as st
import pandas as pd
from common import data_requests


def get_percentage_of_string(string) -> float | None:
    return float(string.strip("%")) / 100 if string is not None else None


def apply_change(value: float, percentage_change: float) -> float:
    return value + (value * percentage_change)


def get_prices_df(item_info: dict) -> pd.DataFrame:
    df = pd.DataFrame(item_info)
    df.reset_index(inplace=True)
    df.rename({
        'index': 'date',
        'average': '30 day average'
    },
              inplace=True,
              axis='columns')
    return df


# Sidebar
curr_category = st.sidebar.selectbox("Item Category",
                                     data_requests.get_categories(),
                                     index=None)
cat_items = data_requests.get_category_items(curr_category)

selected_item = st.sidebar.selectbox(
    "Category Items", [item_info['name'] for item_info in cat_items],
    index=None)

# Main body
selected_item_id = None
if selected_item is not None:
    selected_item_id = [
        item_info for item_info in cat_items
        if item_info['name'] == selected_item
    ][0]['id']
    item_info = data_requests.get_item_info(selected_item_id)
    # st.write(item_info)
    st.title(f"{item_info.get('name', None)}")
    col1, col2 = st.columns(spec=2, gap="small", vertical_alignment="top")
    with col1:
        image_url = item_info.get('icon_large', None)
        if image_url:
            st.image(image_url, use_column_width='always')
        else:
            st.caption(item_info.get('description', None))

    with col2:
        st.write(f"{item_info.get('description', None)}")
        st.write(f"ID: {selected_item_id}")
        st.write(f"Type: {curr_category}")
        member = 'Yes' if item_info.get('members', "") == 'true' else 'No'
        st.write(f"Member only: {member}")

    st.header("Price", divider=True)

    item_prices = data_requests.get_item_historical_prices(selected_item_id)
    prices_df = get_prices_df(item_prices)
    st.line_chart(data=prices_df, x='date', y=['daily', '30 day average'])
