from pydantic import BaseModel, Field

class ItemUpdateResponse(BaseModel):
    id: str = Field(None, example="3")
    header: str = Field(..., example="header")