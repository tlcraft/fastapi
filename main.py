import time
from database_mock import fake_users_db
from datetime import datetime, timedelta
from enum import Enum
from fastapi import Body, Depends, FastAPI, Header, HTTPException, Path, Query, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from models.token import Token
from models.token_data import TokenData
from models.user import User
from models.user_db import UserDB
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from typing import Optional

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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


app = FastAPI(dependencies=[Depends(yield_dependency_example)])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_db_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_db_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_db_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/token", response_model=Token, tags=["auth"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=User, tags=["auth"])
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/users/me/items/", tags=["auth"])
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]

# path operations are evaluated in the order they are defined
# consider your routes and path parameters

@app.get("/", tags=["root"])
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

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response