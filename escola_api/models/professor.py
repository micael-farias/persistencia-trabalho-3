from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from .base import PyObjectId

class ProfessorBase(BaseModel):
    nome: str = Field(..., min_length=3)
    cpf: str = Field(..., min_length=11, max_length=11)
    data_nascimento: datetime
    email: str
    telefone: str
    departamento: str

class ProfessorModel(ProfessorBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True