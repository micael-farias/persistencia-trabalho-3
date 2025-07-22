from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId
from .base import PyObjectId

class DisciplinaBase(BaseModel):
    nome: str = Field(...)
    carga_horaria: int = Field(..., gt=0)
    ementa: str
    professor_responsavel_id: Optional[PyObjectId] = None

class UpdateDisciplinaModel(BaseModel):
    nome: Optional[str] = None
    carga_horaria: Optional[int] = None
    ementa: Optional[str] = None
    professor_responsavel_id: Optional[PyObjectId] = None

class DisciplinaModel(DisciplinaBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )
