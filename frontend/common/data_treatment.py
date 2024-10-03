def treat_monetary_value(item_price: str) -> float:
    if item_price is not None:
        item_price = str(item_price).replace("k", "00")
        item_price = item_price.replace("m", "00000")
        item_price = item_price.replace("b", "00000000")
        item_price = item_price.replace(",", "").replace(".", "")
        item_price = item_price.replace(" ", "")
        item_price = float(item_price)
        return item_price
    else:
        return None