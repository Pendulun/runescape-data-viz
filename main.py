from enum import Enum
from typing import Annotated, Union

from fastapi import FastAPI, Query, Path
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


@app.get("/items/")
async def read_items(q: Annotated[
    str | None,
    Query(
        min_length=3,
        max_length=50,
        title="Query string",
        description=
        "Query string for the items to search in the database that have a good match",
        deprecated=True,
    )] = None,
                     list_param: Annotated[Union[list[str], None],
                                           Query()] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    if list_param:
        results.update({"list_param": list_param})
    return results


@app.get("/items/{item_id}")
async def read_item(
        item_id: Annotated[int, Path(title="The ID of the item to get", ge=1, le=1000)],
        q: Annotated[Union[str, None], Query(alias="item-query")] = None,
        short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({
            "description":
            "This is an amazing item that has a long description"
        })
    return item


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int,
                         item_id: str,
                         needy: str,
                         q: str | None = None,
                         short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id, 'needy': needy}
    if q:
        item.update({"q": q})
    if not short:
        item.update({
            "description":
            "This is an amazing item that has a long description"
        })
    return item


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result
