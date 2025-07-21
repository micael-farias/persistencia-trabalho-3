from .base_repository import BaseRepository
from models import ProfessorModel
from database import professor_collection

class ProfessorRepository(BaseRepository):
    def __init__(self):
        super().__init__(collection=professor_collection, model=ProfessorModel)