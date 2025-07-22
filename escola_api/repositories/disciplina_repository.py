from .base_repository import BaseRepository
from models import DisciplinaModel
from database import disciplina_collection
from typing import Optional, List

class DisciplinaRepository(BaseRepository):
    def __init__(self):
        super().__init__(collection=disciplina_collection, model=DisciplinaModel)

    async def search(
        self,
        nome: Optional[str] = None,
        ementa: Optional[str] = None,
        carga_horaria_min: Optional[int] = None,
        carga_horaria_max: Optional[int] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> List[DisciplinaModel]:
        query_filter = {}
        if nome:
            query_filter["nome"] = {"$regex": nome, "$options": "i"}
        if ementa:
            query_filter["ementa"] = {"$regex": ementa, "$options": "i"}

        if carga_horaria_min is not None or carga_horaria_max is not None:
            carga_filter = {}
            if carga_horaria_min is not None:
                carga_filter["$gte"] = carga_horaria_min
            if carga_horaria_max is not None:
                carga_filter["$lte"] = carga_horaria_max
            query_filter["carga_horaria"] = carga_filter
            
        return await self.find(query_filter, skip=skip, limit=limit)