from typing import List
from pydantic import BaseModel, Field
from bson import ObjectId
from .base import PyObjectId

class HorarioEmbutido(BaseModel):
    dia_semana: str
    horario_inicio: str
    horario_fim: str

class TurmaBase(BaseModel):
    serie_ano: str = Field(...)
    turno: str
    sala: str
    ano_letivo: int
    horarios: List[HorarioEmbutido] = []
    disciplinas_ids: List[PyObjectId] = []

class TurmaModel(TurmaBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True