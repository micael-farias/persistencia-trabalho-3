from .base_repository import BaseRepository
from models import ProfessorModel
from database import professor_collection
from typing import Optional, List
from models.complex_models import DesempenhoProfessorModel
from bson import ObjectId

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

    async def get_desempenho_por_disciplina(self, professor_id: str) -> Optional[DesempenhoProfessorModel]:
        if not ObjectId.is_valid(professor_id):
            return None
            
        pipeline = [
            {'$match': {'_id': ObjectId(professor_id)}},
            
            {'$lookup': {
                'from': 'disciplinas',
                'localField': '_id',
                'foreignField': 'professor_responsavel_id',
                'as': 'desempenho_disciplinas'
            }},
            
            {'$unwind': {
                'path': '$desempenho_disciplinas',
                'preserveNullAndEmptyArrays': True
            }},
            
            {'$lookup': {
                'from': 'notas',
                'localField': 'desempenho_disciplinas._id',
                'foreignField': 'disciplina_id',
                'as': 'notas_da_disciplina'
            }},
            
            {'$addFields': {
                'desempenho_disciplinas.media_geral': {'$avg': '$notas_da_disciplina.valor'},
                'desempenho_disciplinas.total_notas': {'$size': '$notas_da_disciplina'}
            }},
            
            {'$group': {
                '_id': '$_id',
                'doc_original': {'$first': '$$ROOT'},
                'desempenho_disciplinas': {'$push': '$desempenho_disciplinas'}
            }},
            
            {'$project': {
                'nome': '$doc_original.nome',
                'cpf': '$doc_original.cpf',
                'data_nascimento': '$doc_original.data_nascimento',
                'email': '$doc_original.email',
                'telefone': '$doc_original.telefone',
                'departamento': '$doc_original.departamento',
                'desempenho_disciplinas': {
                    '$map': {
                        'input': {
                            '$filter': {
                                'input': '$desempenho_disciplinas',
                                'as': 'd',
                                'cond': '$$d._id' 
                            }
                        },
                        'as': 'd',
                        'in': {
                            '_id': '$$d._id',
                            'nome_disciplina': '$$d.nome',
                            'media_geral': {'$ifNull': ['$$d.media_geral', 0]},
                            'total_notas': '$$d.total_notas'
                        }
                    }
                }
            }}
        ]

        result = await self.collection.aggregate(pipeline).to_list(1)
        if not result:
            return None
            
        return DesempenhoProfessorModel.model_validate(result[0])