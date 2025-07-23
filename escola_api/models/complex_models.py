from pydantic import BaseModel, Field
from typing import List, Optional
from .aluno import AlunoModel
from .disciplina import DisciplinaModel
from .professor import ProfessorModel
from .base import PyObjectId
from .turma import TurmaModel
class ProfessorInfoBoletim(BaseModel):
    nome: str
    email: str

class DisciplinaInfoBoletim(DisciplinaModel):
    professor_info: Optional[ProfessorInfoBoletim] = None

class NotaInfoBoletim(BaseModel):
    id: PyObjectId = Field(alias="_id")
    valor: float
    etapa: str
    disciplina_info: DisciplinaInfoBoletim

class BoletimCompletoModel(AlunoModel):
    notas_detalhadas: List[NotaInfoBoletim] = []

class DesempenhoDisciplina(BaseModel):
    id_disciplina: PyObjectId = Field(alias="_id")
    nome_disciplina: str
    media_geral: float = 0.0
    total_notas: int = 0

class DesempenhoProfessorModel(ProfessorModel):
    desempenho_disciplinas: List[DesempenhoDisciplina] = []

class TurmaComAlunosModel(TurmaModel):
    alunos: List[AlunoModel] = []

class AlunoComTurmaModel(AlunoModel):
    turma: Optional[TurmaModel] = None