from .base_repository import BaseRepository
from models.nota import NotaModel
from database import nota_collection
from typing import Optional, List
from models.base import PyObjectId 

class NotaRepository(BaseRepository):
    def __init__(self):
        super().__init__(collection=nota_collection, model=NotaModel)

    async def search(
        self,
        aluno_id: Optional[PyObjectId] = None,
        disciplina_id: Optional[PyObjectId] = None,
        nota_min: Optional[float] = None,
        nota_max: Optional[float] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> List[NotaModel]:
        query_filter = {}
        if aluno_id:
            query_filter["aluno_id"] = aluno_id
        if disciplina_id:
            query_filter["disciplina_id"] = disciplina_id

        if nota_min is not None or nota_max is not None:
            valor_filter = {}
            if nota_min is not None:
                valor_filter["$gte"] = nota_min
            if nota_max is not None:
                valor_filter["$lte"] = nota_max
            query_filter["valor"] = valor_filter
            
        return await self.find(query_filter, skip=skip, limit=limit)