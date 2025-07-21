from fastapi import APIRouter, Body, status, HTTPException
from models import DisciplinaBase, DisciplinaModel
from repositories import disciplina_repo
from typing import List

router = APIRouter()

@router.get(
    "/",
    response_description="Listar todas as disciplinas",
    response_model=List[DisciplinaModel]
)
async def listar_disciplinas(page: int = 1, limit: int = 10):
    skip = (page - 1) * limit
    disciplinas = await disciplina_repo.get_all(skip=skip, limit=limit)
    return disciplinas
    
@router.post(
    "/",
    response_description="Adicionar nova disciplina",
    response_model=DisciplinaModel,
    status_code=status.HTTP_201_CREATED
)
async def criar_disciplina(disciplina: DisciplinaBase = Body(...)):
    return await disciplina_repo.create(disciplina)

@router.get(
    "/{id}",
    response_description="Buscar disciplina por ID",
    response_model=DisciplinaModel
)
async def buscar_disciplina_por_id(id: str):
    disciplina = await disciplina_repo.get_by_id(id)
    if disciplina:
        return disciplina
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Disciplina com ID {id} não encontrada")