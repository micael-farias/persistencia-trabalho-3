from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic import BaseModel
from bson import ObjectId
from typing import Type, TypeVar, List, Optional

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseRepository:
    def __init__(self, collection: AsyncIOMotorCollection, model: Type[ModelType]):
        self.collection = collection
        self.model = model

    async def create(self, data: CreateSchemaType) -> ModelType:
        doc = data.model_dump(by_alias=True, exclude_none=True)
        result = await self.collection.insert_one(doc)
        created_doc = await self.collection.find_one({"_id": result.inserted_id})
        return self.model.model_validate(created_doc)

    async def get_by_id(self, id: str) -> Optional[ModelType]:
        if not ObjectId.is_valid(id):
            return None
        doc = await self.collection.find_one({"_id": ObjectId(id)})
        if doc:
            return self.model.model_validate(doc)
        return None

    async def get_all(self, skip: int = 0, limit: int = 20) -> List[ModelType]:
        cursor = self.collection.find().skip(skip).limit(limit)
        docs = await cursor.to_list(length=limit)
        return [self.model.model_validate(doc) for doc in docs]

    async def update(self, id: str, data: UpdateSchemaType) -> Optional[ModelType]:
        if not ObjectId.is_valid(id):
            return None
        
        update_data = data.model_dump(exclude_unset=True)

        if not update_data:
            return await self.get_by_id(id)

        await self.collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
        
        updated_doc = await self.get_by_id(id)
        return updated_doc

    async def delete(self, id: str) -> bool:
        if not ObjectId.is_valid(id):
            return False
        
        result = await self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0
