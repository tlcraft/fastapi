from enum import Enum
from typing import Optional
from fastapi import FastAPI

app = FastAPI()

# path operations are evaluated in the order they are defined
# consider your routes and path parameters

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/item/{item_id}")
async def read_item(item_id: int, include_name: bool, include_location: Optional[bool] = None):
    return {
        "item_id": item_id,
        "include_name": include_name,
        "include_location": include_location    
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