import time
from enum import Enum
from typing import Optional
from fastapi import Body, Depends, FastAPI, Header, HTTPException, Path, Query, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field
from user import User

async def verify_test_header(x_test_header: str = Header(...)):
    if x_test_header != "X-Test-Header":
        raise HTTPException(status_code=400, detail="X-Test-Header value invalid")

async def yield_dependency_example():
    try:
        start = time.perf_counter()
        print("Start: ", start)
        yield start
    finally:
        end = time.perf_counter()
        print("End: ", end)
        print(f"Completed the yield in {end - start:0.4f} seconds")


app = FastAPI(dependencies=[Depends(verify_test_header), Depends(yield_dependency_example)])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def fake_decode_token(token: str) -> User:
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user

# path operations are evaluated in the order they are defined
# consider your routes and path parameters

@app.get("/", tags=["Root"])
async def root(current_user: User = Depends(get_current_user)):
    return {"message": "Hello World", "user": current_user}

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

class ItemUpdateResponse(BaseModel):
    id: str = Field(None, example="3")
    header: str = Field(..., example="header")

@app.post("/item/", status_code=status.HTTP_201_CREATED, tags=["items"])
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

@app.put("/items/{item_id}", response_model=ItemUpdateResponse, tags=["items"])
async def update_item(item_id: int, item: Item, x_token: Optional[str] = Header(None)):
    return {"item_id": item_id, "header": x_token, **item.dict()}

@app.get("/item/{item_id}", tags=["items"])
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

@app.get("/models/{model_name}", tags=["models"])
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/models/id/{model_id}", tags=["models"], deprecated=True)
async def get_model_by_id(model_id: int):
    return {"model_id": model_id, "message": "Have some residuals"}


class CommonQueryParams:
    def __init__(self, q: Optional[str] = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


async def common_parameters(commons: CommonQueryParams = Depends(CommonQueryParams), include_all: bool = False):
    return {**commons.__dict__, "include_all": include_all}


@app.get("/users/", tags=["users"])
async def read_users(commons:dict = Depends(common_parameters)):
    return commons


async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


@app.get("/user/{user_id}", dependencies=[Depends(verify_token), Depends(verify_key)], tags=["users"])
async def get_user(user_id):
    return { "user_id": user_id }


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": str(exc)},
    )