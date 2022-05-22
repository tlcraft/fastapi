
from fastapi import APIRouter, Depends, Header, HTTPException

from ..dependencies.dependencies import common_parameters

router = APIRouter(prefix="/users",
    tags=["users"],)

@router.get("/")
async def read_users(commons:dict = Depends(common_parameters)):
    return commons


async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


@router.get("/{user_id}", dependencies=[Depends(verify_token), Depends(verify_key)])
async def get_user(user_id):
    return { "user_id": user_id }
