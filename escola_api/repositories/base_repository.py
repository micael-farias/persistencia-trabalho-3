import logging
from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic import BaseModel
from bson import ObjectId
from typing import Type, TypeVar, List, Optional, Dict, Any

logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseRepository:
    def __init__(self, collection: AsyncIOMotorCollection, model: Type[ModelType]):
        self.collection = collection
        self.model = model
        logger.info(f"Repositório para a coleção '{self.collection.name}' inicializado.")

    async def create(self, data: CreateSchemaType) -> ModelType:
        logger.info(f"Criando novo documento na coleção '{self.collection.name}'")
        doc = data.model_dump(by_alias=True, exclude_none=True)
        result = await self.collection.insert_one(doc)
        created_doc = await self.collection.find_one({"_id": result.inserted_id})
        logger.info(f"Documento criado com ID: {result.inserted_id}")
        return self.model.model_validate(created_doc)

    async def get_by_id(self, id: str) -> Optional[ModelType]:
        logger.info(f"Buscando documento por ID '{id}' na coleção '{self.collection.name}'")
        if not ObjectId.is_valid(id):
            logger.warning(f"Tentativa de busca com ObjectId inválido: {id}")
            return None
        doc = await self.collection.find_one({"_id": ObjectId(id)})
        if doc:
            logger.info(f"Documento com ID '{id}' encontrado.")
            return self.model.model_validate(doc)
        logger.warning(f"Documento com ID '{id}' não encontrado na coleção '{self.collection.name}'.")
        return None

    async def find(self, query: Dict[str, Any], skip: int = 0, limit: int = 20, sort_query: Optional[List[tuple]] = None) -> List[ModelType]:
        logger.info(f"Executando busca na coleção '{self.collection.name}' com filtro: {query}")
        cursor = self.collection.find(query)
        if sort_query:
            logger.info(f"Aplicando ordenação: {sort_query}")
            cursor = cursor.sort(sort_query)
        
        cursor = cursor.skip(skip).limit(limit)
        docs = await cursor.to_list(length=limit)
        logger.info(f"Busca retornou {len(docs)} documentos.")
        return [self.model.model_validate(doc) for doc in docs]

    async def update(self, id: str, data: UpdateSchemaType) -> Optional[ModelType]:
        logger.info(f"Tentando atualizar documento com ID '{id}' na coleção '{self.collection.name}'")
        if not ObjectId.is_valid(id):
            logger.warning(f"Tentativa de atualização com ObjectId inválido: {id}")
            return None
        
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            logger.warning(f"Nenhum dado fornecido para atualização do documento ID '{id}'.")
            return await self.get_by_id(id)

        await self.collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
        logger.info(f"Documento com ID '{id}' atualizado com sucesso.")
        updated_doc = await self.get_by_id(id)
        return updated_doc

    async def delete(self, id: str) -> bool:
        logger.info(f"Tentando deletar documento com ID '{id}' na coleção '{self.collection.name}'")
        if not ObjectId.is_valid(id):
            logger.warning(f"Tentativa de deleção com ObjectId inválido: {id}")
            return False
        
        result = await self.collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count > 0:
            logger.info(f"Documento com ID '{id}' deletado com sucesso.")
            return True
        logger.warning(f"Nenhum documento encontrado para deletar com ID '{id}'.")
        return False

    async def count(self) -> int:
        logger.info(f"Contando documentos na coleção '{self.collection.name}'")
        total = await self.collection.count_documents({})
        logger.info(f"Total de documentos: {total}")
        return total
