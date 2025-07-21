from .base_repository import BaseRepository
from models import DisciplinaModel
from database import disciplina_collection

class DisciplinaRepository(BaseRepository):
    def __init__(self):
        super().__init__(collection=disciplina_collection, model=DisciplinaModel)