# /models/base.py
from typing import Any
from bson import ObjectId
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        
        def validate(v: Any) -> ObjectId:
            if isinstance(v, ObjectId):
                return v
            if ObjectId.is_valid(v):
                return ObjectId(v)
            raise ValueError('ObjectId inválido')

        def serialize(v: ObjectId) -> str:
            return str(v)
        
        # AQUI ESTÁ A CORREÇÃO:
        # Trocamos o validador 'wrap' por 'plain', que espera uma
        # função com apenas um argumento, como a nossa 'validate'.
        python_schema = core_schema.no_info_plain_validator_function(validate)

        serialization_schema = core_schema.plain_serializer_function_ser_schema(
            serialize, when_used='json'
        )

        json_schema = core_schema.str_schema()

        return core_schema.json_or_python_schema(
            python_schema=python_schema,
            json_schema=json_schema,
            serialization=serialization_schema,
        )