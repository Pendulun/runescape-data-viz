import streamlit as st
import pandas as pd
from common import data_requests


def treat_monetary_value(item_price: str) -> float:
    if item_price is not None:
        item_price = str(item_price).replace("k", "00")
        item_price = item_price.replace(",", "").replace(".", "")
        item_price = item_price.replace(" ", "")
        item_price = float(item_price)
        return item_price
    else:
        return None


def get_percentage_of_string(string) -> float | None:
    return float(string.strip("%")) / 100 if string is not None else None


def apply_change(value: float, percentage_change: float) -> float:
    return value + (value * percentage_change)


def get_historical_prices(item_info: dict) -> pd.DataFrame:
    prices = list()
    dates = list()

    last_day_price = treat_monetary_value(
        item_info.get('current', dict()).get('price', None))

    today_price_change = treat_monetary_value(
        item_info.get('today', dict()).get('price', None))
    today_price = last_day_price + today_price_change

    periods_prices = dict()
    for period in ['day30', 'day90', 'day180']:
        period_change = item_info.get(period, dict()).get('change', None)
        period_percentage_change = get_percentage_of_string(period_change)
        period_price = None
        if period_change and last_day_price is not None:
            period_price = apply_change(last_day_price,
                                        period_percentage_change)
        periods_prices[period] = period_price

    prices.extend([
        periods_prices['day180'], periods_prices['day90'],
        periods_prices['day30'], last_day_price, today_price
    ])
    dates.extend(
        ['180 days ago', '90 days ago', '30 days ago', 'yesterday', 'today'])

    df = pd.DataFrame()
    df['prices'] = prices
    df['dates'] = dates
    return df


curr_category = st.sidebar.selectbox("Item Category",
                                     data_requests.get_categories(),
                                     index=None)
cat_items = data_requests.get_category_items(curr_category)

selected_item = st.sidebar.selectbox(
    "Category Items", [item_info['name'] for item_info in cat_items],
    index=None)

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

    st.header("Price", divider=True)

    # st.write(f"30 days ago: {periods_prices['day30']:.2f}")
    # st.write(f"90 days ago: {periods_prices['day90']:.2f}")
    # st.write(f"180 days ago: {periods_prices['day180']:.2f}")

    prices_df = get_historical_prices(item_info)
    st.line_chart(data=prices_df, x='dates', y='prices')
