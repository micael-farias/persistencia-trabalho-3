from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from .base import PyObjectId

class AlunoBase(BaseModel):
    nome: str = Field(..., min_length=3)
    cpf: str = Field(..., min_length=11, max_length=11)
    data_nascimento: datetime
    email: str
    telefone: str
    matricula: str = Field(..., unique=True)
    ano_escolar: int = Field(..., ge=1, le=3)
    turma_id: Optional[PyObjectId] = None

class AlunoModel(AlunoBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True