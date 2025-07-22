from fastapi import APIRouter, Body, status, HTTPException
from typing import List
from models.aluno import AlunoBase, AlunoModel, UpdateAlunoModel
from repositories import aluno_repo

router = APIRouter()

@router.get("/count", response_model=dict)
async def contar_alunos():
    total = await aluno_repo.count()
    return {"total_de_alunos": total}

@router.post("/", response_model=AlunoModel, status_code=status.HTTP_201_CREATED)
async def criar_aluno(aluno: AlunoBase = Body(...)):
    return await aluno_repo.create(aluno)

@router.get("/", response_model=List[AlunoModel])
async def listar_alunos(page: int = 1, limit: int = 10):
    skip = (page - 1) * limit
    return await aluno_repo.get_all(skip=skip, limit=limit)

@router.get("/{id}", response_model=AlunoModel)
async def buscar_aluno_por_id(id: str):
    aluno = await aluno_repo.get_by_id(id)
    if aluno:
        return aluno
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Aluno com ID {id} não encontrado")

@router.put("/{id}", response_model=AlunoModel)
async def atualizar_aluno(id: str, aluno_update: UpdateAlunoModel = Body(...)):
    aluno_atualizado = await aluno_repo.update(id, aluno_update)
    if aluno_atualizado:
        return aluno_atualizado
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Aluno com ID {id} não encontrado")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_aluno(id: str):
    deletado = await aluno_repo.delete(id)
    if not deletado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Aluno com ID {id} não encontrado")
    return