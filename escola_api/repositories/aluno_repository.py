from .base_repository import BaseRepository
from models import AlunoModel
from database import aluno_collection
from typing import Optional, List
from models.complex_models import BoletimCompletoModel
from bson import ObjectId
from pymongo import ASCENDING
from datetime import datetime

class AlunoRepository(BaseRepository):
    def __init__(self):
        super().__init__(collection=aluno_collection, model=AlunoModel)
    
    async def search(
        self,
        nome: Optional[str] = None, 
        ano_escolar: Optional[int] = None,
        data_nascimento_inicio: Optional[datetime] = None,
        data_nascimento_fim: Optional[datetime] = None,
        sort_by: Optional[str] = None,
        sort_order: int = ASCENDING,
        skip: int = 0, 
        limit: int = 20
    ) -> List[AlunoModel]:
        query_filter = {}
        if nome:
            query_filter["nome"] = {"$regex": nome, "$options": "i"}
        if ano_escolar is not None:
            query_filter["ano_escolar"] = ano_escolar
        
        if data_nascimento_inicio or data_nascimento_fim:
            date_filter = {}
            if data_nascimento_inicio:
                date_filter["$gte"] = data_nascimento_inicio
            if data_nascimento_fim:
                date_filter["$lte"] = data_nascimento_fim
            query_filter["data_nascimento"] = date_filter
        
        sort_query = []
        if sort_by:
            sort_query.append((sort_by, sort_order))
        
        return await self.find(query_filter, skip=skip, limit=limit, sort_query=sort_query)

    async def get_boletim_detalhado(self, aluno_id: str) -> Optional[BoletimCompletoModel]:
        if not ObjectId.is_valid(aluno_id):
            return None

        pipeline = [
            {'$match': {'_id': ObjectId(aluno_id)}},
            
            {'$lookup': {
                'from': 'notas',
                'localField': '_id',
                'foreignField': 'aluno_id',
                'as': 'notas_detalhadas'
            }},
            
            {'$unwind': '$notas_detalhadas'},
            
            {'$lookup': {
                'from': 'disciplinas',
                'localField': 'notas_detalhadas.disciplina_id',
                'foreignField': '_id',
                'as': 'notas_detalhadas.disciplina_info'
            }},
            
            {'$unwind': '$notas_detalhadas.disciplina_info'},
            
            {'$lookup': {
                'from': 'professores',
                'localField': 'notas_detalhadas.disciplina_info.professor_responsavel_id',
                'foreignField': '_id',
                'as': 'notas_detalhadas.disciplina_info.professor_info'
            }},
            
            {'$unwind': {'path': '$notas_detalhadas.disciplina_info.professor_info', 'preserveNullAndEmptyArrays': True}},
            
            {'$group': {
                '_id': '$_id',
                'doc_original': {'$first': '$$ROOT'},
                'notas_detalhadas': {'$push': '$notas_detalhadas'}
            }},
            
            {'$replaceRoot': {
                'newRoot': {
                    '$mergeObjects': ['$doc_original', {'notas_detalhadas': '$notas_detalhadas'}]
                }
            }}
        ]

        result = await self.collection.aggregate(pipeline).to_list(1)
        if not result:
            return None
        
        return BoletimCompletoModel.model_validate(result[0])