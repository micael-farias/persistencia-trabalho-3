from fastapi import APIRouter, Body, status, HTTPException
from typing import List
from models.turma import TurmaBase, TurmaModel, UpdateTurmaModel
from repositories import turma_repo

router = APIRouter()

@router.post("/", response_model=TurmaModel, status_code=status.HTTP_201_CREATED)
async def criar_turma(turma: TurmaBase = Body(...)):
    return await turma_repo.create(turma)

@router.get("/", response_model=List[TurmaModel])
async def listar_turmas(page: int = 1, limit: int = 10):
    skip = (page - 1) * limit
    return await turma_repo.get_all(skip=skip, limit=limit)

@router.get("/{id}", response_model=TurmaModel)
async def buscar_turma_por_id(id: str):
    turma = await turma_repo.get_by_id(id)
    if turma:
        return turma
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Turma com ID {id} não encontrada")

@router.put("/{id}", response_model=TurmaModel)
async def atualizar_turma(id: str, turma_update: UpdateTurmaModel = Body(...)):
    turma_atualizada = await turma_repo.update(id, turma_update)
    if turma_atualizada:
        return turma_atualizada
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Turma com ID {id} não encontrada")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_turma(id: str):
    deletado = await turma_repo.delete(id)
    if not deletado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Turma com ID {id} não encontrada")
    return