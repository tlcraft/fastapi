from enum import Enum
from typing import Optional
from fastapi import Body, FastAPI, Header, Path, Query, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI()

# path operations are evaluated in the order they are defined
# consider your routes and path parameters

@app.get("/")
async def root():
    return {"message": "Hello World"}

class Item(BaseModel):
    id: str = Field(None, example="3")
    type: str = Field(..., example="Foo")
    description: Optional[str] = Field(None, example="A very nice Item")
    price: float = Field(..., example=35.4)
    tax: Optional[float] = Field(None, example=3.2)
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
async def create_item(
    payload: Item = Body(..., example={
            "type": "Foo",
            "description": "A very nice Item",
            "price": 35.4,
            "tax": 3.23,
        },
    )
): 
    payload.id = 1
    return payload

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, x_token: Optional[str] = Header(None)):
    return {"item_id": item_id, "header": x_token, **item.dict()}

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


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": str(exc)},
    )