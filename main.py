from enum import Enum
from typing import Optional
from fastapi import FastAPI, Path, Query
from pydantic import BaseModel

app = FastAPI()

# path operations are evaluated in the order they are defined
# consider your routes and path parameters

@app.get("/")
async def root():
    return {"message": "Hello World"}

class Item(BaseModel):
    id: str
    type: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    class Config:
        schema_extra = {
            "example": {
                "id": 3,
                "type": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }

@app.post("/item/")
async def create_item(payload: Item):
    return payload

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}

@app.get("/item/{item_id}")
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

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}