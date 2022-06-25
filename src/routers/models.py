from fastapi import APIRouter
from src.enums.model_name import ModelName

router = APIRouter(prefix="/models", tags=["models"])
    
@router.get("/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@router.get("/id/{model_id}", deprecated=True)
async def get_model_by_id(model_id: int):
    return {"model_id": model_id, "message": "Have some residuals"}