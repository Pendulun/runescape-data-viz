import copy
from datetime import datetime

import streamlit as st
from common import data_requests_wrapper, data_treatment


def augment_data(items: list[dict]) -> list[dict]:
    items_copy = copy.deepcopy(items)
    for item in items_copy:
        item['treated_current_price'] = data_treatment.treat_monetary_value(
            item['current']['price'])
        item[
            'treated_today_price_change'] = data_treatment.treat_monetary_value(
                item['today']['price'])
        item['relative_change'] = (item['treated_today_price_change'] /
                                   item['treated_current_price']) * 100

    return items_copy


def format_item_info(item_info: dict) -> dict:
    target_info = dict()
    target_info['name'] = item_info['name']
    target_info['treated_price'] = item_info['treated_current_price']
    target_info['original_price'] = item_info['current']['price']
    target_info['price_change'] = item_info['treated_today_price_change']
    target_info['relative_change'] = item_info['relative_change']
    target_info['icon'] = item_info['icon_large']
    return target_info


def get_top_n_by_col_and_filter(items: list[dict],
                                top_n: int,
                                target_col: str,
                                reverse: bool,
                                filter: str = None) -> list[dict]:
    sorted_items = sorted(items, key=lambda i: i[target_col], reverse=reverse)
    if filter == "negatives":
        sorted_items = [item for item in sorted_items if item[target_col] < 0]
    elif filter == "positives":
        sorted_items = [item for item in sorted_items if item[target_col] > 0]
    top_n_items = [format_item_info(item) for item in sorted_items[:top_n]]
    return top_n_items


def get_top_prices(items: list[dict], top_n: int = 5) -> list[dict]:
    treated_items = augment_data(items)
    target_items = get_top_n_by_col_and_filter(treated_items,
                                               top_n,
                                               'treated_current_price',
                                               reverse=True)
    return target_items


def get_top_prices_increases_abs(items: list[dict],
                                 top_n: int = 5) -> list[dict]:
    treated_items = augment_data(items)
    target_items = get_top_n_by_col_and_filter(treated_items,
                                               top_n,
                                               'treated_today_price_change',
                                               reverse=True,
                                               filter='positives')
    return target_items


def get_top_prices_increases_relative(items: list[dict],
                                      top_n: int = 5) -> list[dict]:
    treated_items = augment_data(items)
    target_items = get_top_n_by_col_and_filter(treated_items,
                                               top_n,
                                               'relative_change',
                                               reverse=True,
                                               filter='positives')
    return target_items


def get_top_prices_decreases_abs(items: list[dict],
                                 top_n: int = 5) -> list[dict]:
    treated_items = augment_data(items)
    target_items = get_top_n_by_col_and_filter(treated_items,
                                               top_n,
                                               'treated_today_price_change',
                                               reverse=False,
                                               filter='negatives')
    return target_items


def get_top_prices_decreases_relative(items: list[dict],
                                      top_n: int = 5) -> list[dict]:
    treated_items = augment_data(items)
    target_items = get_top_n_by_col_and_filter(treated_items,
                                               top_n,
                                               'relative_change',
                                               reverse=False,
                                               filter="negatives")
    return target_items


def show_simple_list(filter_func,
                     items: list[dict],
                     max_cols: int,
                     names_cols: list,
                     info_cols: list,
                     more_info: bool = False):
    target_items = filter_func(items, top_n=max_cols)
    for col_id, name_col in enumerate(names_cols):
        if col_id < len(target_items):
            item_info = target_items[col_id]
            name_col.write(item_info['name'])
            info_col = info_cols[col_id]
            info_col.image(item_info['icon'], use_column_width='always')
            info_col.write(f"Current price: {item_info['original_price']}")
            if more_info:
                info_col.write(f"Price Change: {item_info['price_change']}")
                info_col.write(
                    f"Relative Change: {item_info['relative_change']:.2f}%")
        else:
            name_col.write(None)


# Sidebar
categories = data_requests_wrapper.get_categories()
curr_category = st.sidebar.selectbox("Item Category", categories, index=None)

# Main body
if curr_category is not None:
    cat_items = data_requests_wrapper.get_category_items(
        curr_category,
        datetime.today().date())

    st.title(curr_category.title())
    st.write(f"Num of items: {len(cat_items)}")

    max_top_n = 4
    infos_to_show = [{
        "title": f"Today Top {max_top_n} prices",
        "func": get_top_prices,
        'more_info': False
    }, {
        "title": f"Today Top {max_top_n} prices increases (absolute)",
        "func": get_top_prices_increases_abs,
        'more_info': True
    }, {
        "title": f"Today Top {max_top_n} prices increases (relative)",
        "func": get_top_prices_increases_relative,
        'more_info': True
    }, {
        "title": f"Today Top {max_top_n} prices decreases (absolute)",
        "func": get_top_prices_decreases_abs,
        'more_info': True
    }, {
        "title": f"Today Top {max_top_n} prices decreases (relative)",
        "func": get_top_prices_decreases_relative,
        'more_info': True
    }]

    for info in infos_to_show:
        st.subheader(info['title'])
        names_cols = st.columns(spec=max_top_n,
                                gap="small",
                                vertical_alignment="top")
        info_cols = st.columns(spec=max_top_n,
                               gap="small",
                               vertical_alignment="top")
        show_simple_list(info['func'],
                         cat_items,
                         max_top_n,
                         names_cols,
                         info_cols,
                         more_info=info['more_info'])
