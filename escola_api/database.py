import os
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str
    DB_NAME: str

    class Config:
        env_file = ".env"

settings = Settings()

client = AsyncIOMotorClient(settings.MONGO_URI)
db = client[settings.DB_NAME]

aluno_collection = db.get_collection("alunos")
professor_collection = db.get_collection("professores")
disciplina_collection = db.get_collection("disciplinas")
turma_collection = db.get_collection("turmas")
nota_collection = db.get_collection("notas")