from .base_repository import BaseRepository
from models.nota import NotaModel
from database import nota_collection

class NotaRepository(BaseRepository):
    def __init__(self):
        super().__init__(collection=nota_collection, model=NotaModel)