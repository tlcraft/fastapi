import time
from src.dependencies.dependencies import yield_dependency_example
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .routers import auth, items, models, notifications, users

description = """
OverviewApp API is an example API that helps demonstrate various aspects of FastAPI. 🚀

## Auth

You can login and retrieve an auth token.

## Items

You can **read items**, **update items**, and **create items**.

## Models

You can get a model by name or get a model by id.

## Notifications

You can send a notification by email.

## Root

You can retrieve a simple hello world object.

## Users

You will be able to:

* **Read a user by id**
* **Read users**
* **Get the authenticated user's own information**
* **Get the authenticated user's own items**
"""

tags_metadata = [
    {
        "name": "auth",
        "description": "Operations for authentication.",
    },
    {
        "name": "items",
        "description": "Operations for items.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
    {
        "name": "models",
        "description": "Operations for models.",
    },
        {
        "name": "notifications",
        "description": "Operations for notifcations.",
    },
    {
        "name": "root",
        "description": "Operations at the root of the API.",
    },
    {
        "name": "users",
        "description": "Operations for users.",
    },
]

app = FastAPI(    
    title="OverviewApp",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "First Last",
        "url": "http://www.example.com/contact/",
        "email": "first.last@example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    dependencies=[Depends(yield_dependency_example)],
    openapi_tags=tags_metadata,
    openapi_url="/api/v1/openapi.json",
    docs_url="/documentation",
    redoc_url=None
)

app.include_router(auth.router)
app.include_router(items.router)
app.include_router(models.router)
app.include_router(notifications.router)
app.include_router(users.router)

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

# path operations are evaluated in the order they are defined
# consider your routes and path parameters

@app.get("/", tags=["root"])
async def root():
    return {"message": "Hello World"}

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