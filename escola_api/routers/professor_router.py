from fastapi import APIRouter, Body, status, HTTPException
from models import ProfessorBase, ProfessorModel
from repositories import professor_repo
from typing import List

router = APIRouter()

@router.get(
    "/",
    response_description="Listar todos os professores",
    response_model=List[ProfessorModel]
)
async def listar_professores(page: int = 1, limit: int = 10):
    skip = (page - 1) * limit
    professores = await professor_repo.get_all(skip=skip, limit=limit)
    return professores

@router.post(
    "/",
    response_description="Adicionar novo professor",
    response_model=ProfessorModel,
    status_code=status.HTTP_201_CREATED
)
async def criar_professor(professor: ProfessorBase = Body(...)):
    return await professor_repo.create(professor)

@router.get(
    "/{id}",
    response_description="Buscar professor por ID",
    response_model=ProfessorModel
)
async def buscar_professor_por_id(id: str):
    professor = await professor_repo.get_by_id(id)
    if professor:
        return professor
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Professor com ID {id} não encontrado")