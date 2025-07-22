from typing import Optional
from datetime import datetime
from pydantic import Field, BaseModel, ConfigDict
from bson import ObjectId
from .base import PyObjectId

class AlunoBase(BaseModel):
    nome: str = Field(..., min_length=3)
    cpf: str = Field(..., min_length=11, max_length=11)
    data_nascimento: datetime
    email: str
    telefone: str
    matricula: str = Field(...)
    ano_escolar: int = Field(..., ge=1, le=3)
    turma_id: Optional[PyObjectId] = None

class UpdateAlunoModel(BaseModel):
    nome: Optional[str] = None
    cpf: Optional[str] = None
    data_nascimento: Optional[datetime] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    matricula: Optional[str] = None
    ano_escolar: Optional[int] = None
    turma_id: Optional[PyObjectId] = None

class AlunoModel(AlunoBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )