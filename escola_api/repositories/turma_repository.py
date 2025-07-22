from .base_repository import BaseRepository
from models import TurmaModel
from database import turma_collection
from typing import Optional, List

class TurmaRepository(BaseRepository):
    def __init__(self):
        super().__init__(collection=turma_collection, model=TurmaModel)

    async def search(
        self,
        serie_ano: Optional[str] = None,
        turno: Optional[str] = None,
        ano_letivo: Optional[int] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> List[TurmaModel]:
        query_filter = {}
        if serie_ano:
            query_filter["serie_ano"] = {"$regex": serie_ano, "$options": "i"}
        if turno:
            query_filter["turno"] = turno
        if ano_letivo is not None:
            query_filter["ano_letivo"] = ano_letivo
            
        return await self.find(query_filter, skip=skip, limit=limit)
