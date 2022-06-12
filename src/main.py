import time
from dependencies.dependencies import yield_dependency_example
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .routers import auth, items, models, notifications, users

app = FastAPI(dependencies=[Depends(yield_dependency_example)])
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