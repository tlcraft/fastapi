from fastapi import APIRouter, Body, Header, Path, Query, status
from fastapi.encoders import jsonable_encoder
from src.models.item import Item
from src.models.item_update_response import ItemUpdateResponse
from typing import Optional

router = APIRouter(prefix="/items", tags=["items"])

@router.post("/item/", status_code=status.HTTP_201_CREATED)
async def create_item(
    payload: Item = Body(..., example={
            "type": "Foo",
            "description": "A very nice Item",
            "price": 35.4,
            "tax": 3.23,
        },
    )
):
    """
    Create an item with all the information:

    - **type**: each item must have a type
    - **description**: a description of the item
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    """
    payload.id = 1
    json_encoded = jsonable_encoder(payload)
    print("JSON Encoded: ", json_encoded)
    print("ID: ", json_encoded["id"])
    return json_encoded

@router.put("/items/{item_id}", response_model=ItemUpdateResponse)
async def update_item(item_id: int, item: Item, x_token: Optional[str] = Header(None)):
    return {"item_id": item_id, "header": x_token, **item.dict()}

@router.get("/item/{item_id}")
async def read_item(
    include_name: bool, 
    item_id: int = Path(..., title="The ID of the item to get."), 
    include_create_date: bool = True, 
    include_location: Optional[bool] = None, 
    query: str = Query(None, min_length=3, max_length=8, title="query", description="Example query parameter.")
):
    return {
        "item_id": item_id,
        "include_name": include_name,
        "include_create_date": include_create_date,
        "include_location": include_location,
        "query": query  
    }