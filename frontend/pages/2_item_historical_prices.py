import streamlit as st
import pandas as pd
from common import data_requests_wrapper
from common.predict import augment_with_predictions


def get_percentage_of_string(string) -> float | None:
    return float(string.strip("%")) / 100 if string is not None else None


def apply_change(value: float, percentage_change: float) -> float:
    return value + (value * percentage_change)


@st.cache_data
def get_prices_df(item_id: int) -> pd.DataFrame:
    item_prices = data_requests_wrapper.get_item_historical_prices(item_id)
    df = pd.DataFrame(item_prices)
    df.reset_index(inplace=True)
    df.rename({
        'index': 'date',
        'average': '30 day average'
    },
              inplace=True,
              axis='columns')
    df.set_index("date", drop=True, inplace=True)
    df.index = pd.DatetimeIndex(pd.to_datetime(df.index, format="%Y-%m-%d"),
                                freq='infer')
    return df


@st.cache_data()
def get_prices_with_predictions(item_id: int, selected_models: list[str],
                                forward_days: int):
    prices_df = get_prices_df(item_id)
    augmented_df, best_model_name, best_model_params, test_error = augment_with_predictions(
        prices_df, selected_models, forward_days)
    return augmented_df, best_model_name, best_model_params, test_error


# Sidebar
curr_category = st.sidebar.selectbox("Item Category",
                                     data_requests_wrapper.get_categories(),
                                     index=None)
cat_items = data_requests_wrapper.get_category_items(curr_category)

selected_item = st.sidebar.selectbox(
    "Category Items", [item_info['name'] for item_info in cat_items],
    index=None)

# Main body
selected_item_id = None
prices_df = None
if selected_item is not None:
    selected_item_id = [
        item_info for item_info in cat_items
        if item_info['name'] == selected_item
    ][0]['id']
    item_info = data_requests_wrapper.get_item_info(selected_item_id)

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
    selected_models = st.multiselect("Predict with (only the best is used)",
                                     ['ARIMA', 'AutoARIMA', 'Prophet'])
    forward_days = st.select_slider(
        "Num of days to predict",
        options=[
            1,
            7,
            14,
            21,
        ],
    )

    try:
        augmented_df, best_model_name, best_model_params, test_error = get_prices_with_predictions(
            selected_item_id, selected_models, forward_days)
    except Exception as e:
        st.exception(e)
    else:
        if len(selected_models) > 0:
            best_result_msg = f"Best model: {best_model_name} with params: {best_model_params}"
            best_result_msg += f" and test error (RMSE): {test_error:.2f}"
            st.write(best_result_msg)

            st.write(
                f"{item_info.get('name', None)} historical prices and predictions"
            )
            st.line_chart(
                data=augmented_df,
                x=None,
                y=['daily', '30 day average', 'Test Pred', 'future_price'])
            GE_url = "https://secure.runescape.com/m=itemdb_rs/results"
            st.markdown(
                f"Search for the real price at the [Grand Exchange]({GE_url})")
            st.write("Predicted prices")
            st.write(augmented_df[~augmented_df['future_price'].isna()]
                     ['future_price'])
        else:
            st.write(f"{item_info.get('name', None)} historical prices")
            st.line_chart(data=augmented_df,
                          x=None,
                          y=['daily', '30 day average'])
