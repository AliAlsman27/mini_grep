from pydantic import BaseModel, Field
from typing import Optional
from bson.objectid import ObjectId


class DataChunk(BaseModel):
    
    _id: optional[ObjectId]
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: dict = Field(..., min_length=1)
    chunk_order: int = Field(..., gt=0)
    chunk_project_id: objectId



    class Config:
        arbitrary_types_allowed = True
        