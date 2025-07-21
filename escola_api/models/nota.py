from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId
from .base import PyObjectId

class NotaBase(BaseModel):
    valor: float = Field(..., ge=0, le=10)
    etapa: str = Field(..., min_length=3) # Ex: "1º Bimestre"
    data_lancamento: datetime
    aluno_id: PyObjectId
    disciplina_id: PyObjectId

class NotaModel(NotaBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={
            ObjectId: str
        },
    )