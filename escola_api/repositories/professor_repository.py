from .base_repository import BaseRepository
from models import ProfessorModel
from database import professor_collection
from typing import Optional, List

class ProfessorRepository(BaseRepository):
    def __init__(self):
        super().__init__(collection=professor_collection, model=ProfessorModel)

    async def search(
        self, 
        nome: Optional[str] = None,
        email: Optional[str] = None,
        telefone: Optional[str] = None,
        departamento: Optional[str] = None, 
        skip: int = 0, 
        limit: int = 20
    ) -> List[ProfessorModel]:
        query_filter = {}
        if nome:
            query_filter["nome"] = {"$regex": nome, "$options": "i"}
        if email:
            query_filter["email"] = {"$regex": email, "$options": "i"}
        if telefone:
            query_filter["telefone"] = {"$regex": telefone, "$options": "i"}
        if departamento:
            query_filter["departamento"] = {"$regex": departamento, "$options": "i"}
        
        return await self.find(query_filter, skip=skip, limit=limit)