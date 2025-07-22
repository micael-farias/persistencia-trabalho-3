from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
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

class UpdateTurmaModel(BaseModel):
    serie_ano: Optional[str] = None
    turno: Optional[str] = None
    sala: Optional[str] = None
    ano_letivo: Optional[int] = None
    horarios: Optional[List[HorarioEmbutido]] = None
    disciplinas_ids: Optional[List[PyObjectId]] = None

class TurmaModel(TurmaBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )