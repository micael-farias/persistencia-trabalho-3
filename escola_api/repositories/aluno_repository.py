from .base_repository import BaseRepository
from models import AlunoModel
from database import aluno_collection
from typing import Optional, List

class AlunoRepository(BaseRepository):
    def __init__(self):
        super().__init__(collection=aluno_collection, model=AlunoModel)
    
    async def search(
            self, 
            nome: Optional[str] = None, 
            ano_escolar: Optional[int] = None, 
            skip: int = 0, 
            limit: int = 20
        ) -> List[AlunoModel]:
            query_filter = {}
            if nome:
                query_filter["nome"] = {"$regex": nome, "$options": "i"}
            if ano_escolar is not None:
                query_filter["ano_escolar"] = ano_escolar
            
            return await self.find(query_filter, skip=skip, limit=limit)