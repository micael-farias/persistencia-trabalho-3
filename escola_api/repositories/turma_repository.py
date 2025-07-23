from .base_repository import BaseRepository
from models import TurmaModel
from database import turma_collection
from typing import Optional, List
from models.complex_models import TurmaComAlunosModel
from bson import ObjectId

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

    async def get_turma_com_alunos(self, turma_id: str) -> Optional[TurmaComAlunosModel]:
        if not ObjectId.is_valid(turma_id):
            return None

        pipeline = [
            {'$match': {'_id': ObjectId(turma_id)}},
            
            {'$lookup': {
                'from': 'alunos',           
                'localField': '_id',         
                'foreignField': 'turma_id',  
                'as': 'alunos'             
            }}
        ]

        result = await self.collection.aggregate(pipeline).to_list(1)
        if not result:
            return None
        
        return TurmaComAlunosModel.model_validate(result[0])
