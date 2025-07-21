from fastapi import APIRouter, Body, status, HTTPException
from models import TurmaBase, TurmaModel
from repositories import turma_repo
from typing import List

router = APIRouter()

@router.get(
    "/",
    response_description="Listar todas as turmas",
    response_model=List[TurmaModel]
)
async def listar_turmas(page: int = 1, limit: int = 10):
    skip = (page - 1) * limit
    turmas = await turma_repo.get_all(skip=skip, limit=limit)
    return turmas

@router.post(
    "/",
    response_description="Adicionar nova turma",
    response_model=TurmaModel,
    status_code=status.HTTP_201_CREATED
)
async def criar_turma(turma: TurmaBase = Body(...)):
    return await turma_repo.create(turma)

@router.get(
    "/{id}",
    response_description="Buscar turma por ID",
    response_model=TurmaModel
)
async def buscar_turma_por_id(id: str):
    turma = await turma_repo.get_by_id(id)
    if turma:
        return turma
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Turma com ID {id} não encontrada")