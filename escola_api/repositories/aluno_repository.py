from .base_repository import BaseRepository
from models import AlunoModel
from database import aluno_collection

class AlunoRepository(BaseRepository):
    def __init__(self):
        super().__init__(collection=aluno_collection, model=AlunoModel)
