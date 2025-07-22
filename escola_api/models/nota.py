from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId
from .base import PyObjectId

class NotaBase(BaseModel):
    valor: float = Field(..., ge=0, le=10)
    etapa: str = Field(..., min_length=3)
    data_lancamento: datetime
    aluno_id: PyObjectId
    disciplina_id: PyObjectId

class UpdateNotaModel(BaseModel):
    valor: Optional[float] = None
    etapa: Optional[str] = None
    data_lancamento: Optional[datetime] = None
    aluno_id: Optional[PyObjectId] = None
    disciplina_id: Optional[PyObjectId] = None

class NotaModel(NotaBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )
