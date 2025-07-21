from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId
from .base import PyObjectId

class DisciplinaBase(BaseModel):
    nome: str = Field(..., unique=True)
    carga_horaria: int = Field(..., gt=0)
    ementa: str
    professor_responsavel_id: Optional[PyObjectId] = None

class DisciplinaModel(DisciplinaBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True