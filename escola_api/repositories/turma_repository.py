from .base_repository import BaseRepository
from models import TurmaModel
from database import turma_collection

class TurmaRepository(BaseRepository):
    def __init__(self):
        super().__init__(collection=turma_collection, model=TurmaModel)