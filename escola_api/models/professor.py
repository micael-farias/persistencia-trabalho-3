from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId
from .base import PyObjectId

class ProfessorBase(BaseModel):
    nome: str = Field(..., min_length=3)
    cpf: str = Field(..., min_length=11, max_length=11)
    data_nascimento: datetime
    email: str
    telefone: str
    id_professor: str = Field(...)
    departamento: str

class UpdateProfessorModel(BaseModel):
    nome: Optional[str] = None
    cpf: Optional[str] = None
    data_nascimento: Optional[datetime] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    id_professor: Optional[str] = None
    departamento: Optional[str] = None

class ProfessorModel(ProfessorBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )
