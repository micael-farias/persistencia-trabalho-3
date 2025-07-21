from fastapi import APIRouter, Body, status, HTTPException
from models import AlunoBase, AlunoModel
from repositories import aluno_repo
from typing import List

router = APIRouter()

@router.get(
    "/",
    response_description="Listar todos os alunos",
    response_model=List[AlunoModel]
)
async def listar_alunos(page: int = 1, limit: int = 10):
    skip = (page - 1) * limit
    alunos = await aluno_repo.get_all(skip=skip, limit=limit)
    return alunos

@router.post(
    "/",
    response_description="Adicionar novo aluno",
    response_model=AlunoModel,
    status_code=status.HTTP_201_CREATED
)
async def criar_aluno(aluno: AlunoBase = Body(...)):
    return await aluno_repo.create(aluno)

@router.get(
    "/{id}",
    response_description="Buscar aluno por ID",
    response_model=AlunoModel
)
async def buscar_aluno_por_id(id: str):
    aluno = await aluno_repo.get_by_id(id)
    if aluno:
        return aluno
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Aluno com ID {id} não encontrado")