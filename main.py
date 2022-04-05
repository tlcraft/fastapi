from fastapi import FastAPI

app = FastAPI()

# path operations are evaluated in the order they are defined
# consider your routes and path parameters

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/item/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}