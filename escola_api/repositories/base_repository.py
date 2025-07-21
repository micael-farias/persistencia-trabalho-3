from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic import BaseModel
from bson import ObjectId
from typing import Type, TypeVar, List, Optional

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)

class BaseRepository:
    def __init__(self, collection: AsyncIOMotorCollection, model: Type[ModelType]):
        self.collection = collection
        self.model = model

    async def create(self, data: CreateSchemaType) -> ModelType:
        doc = data.model_dump(by_alias=True, exclude_none=True)
        result = await self.collection.insert_one(doc)
        created_doc = await self.collection.find_one({"_id": result.inserted_id})
        return self.model(**created_doc)

    async def get_by_id(self, id: str) -> Optional[ModelType]:
        if not ObjectId.is_valid(id):
            return None
        doc = await self.collection.find_one({"_id": ObjectId(id)})
        if doc:
            return self.model(**doc)
        return None

    async def get_all(self, skip: int = 0, limit: int = 20) -> List[ModelType]:
        cursor = self.collection.find().skip(skip).limit(limit)
        docs = await cursor.to_list(length=limit)
        return [self.model(**doc) for doc in docs]