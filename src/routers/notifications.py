from fastapi import APIRouter, BackgroundTasks, Depends
from src.dependencies.dependencies import get_query, write_log

router = APIRouter(prefix="/notifications", tags=["notifications"])
    
@router.post("/send-notification/{email}")
async def send_notification(
    email: str, background_tasks: BackgroundTasks, q: str = Depends(get_query)
):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)
    return {"message": "Message sent"}