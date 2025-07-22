from fastapi import APIRouter, Body, status, HTTPException
from typing import List
from models.disciplina import DisciplinaBase, DisciplinaModel, UpdateDisciplinaModel
from repositories import disciplina_repo

router = APIRouter()

@router.get("/count", response_model=dict)
async def contar_disciplinas():
    total = await disciplina_repo.count()
    return {"total_de_disciplinas": total}
    
@router.post("/", response_model=DisciplinaModel, status_code=status.HTTP_201_CREATED)
async def criar_disciplina(disciplina: DisciplinaBase = Body(...)):
    return await disciplina_repo.create(disciplina)

@router.get("/", response_model=List[DisciplinaModel])
async def listar_disciplinas(page: int = 1, limit: int = 10):
    skip = (page - 1) * limit
    return await disciplina_repo.get_all(skip=skip, limit=limit)

@router.get("/{id}", response_model=DisciplinaModel)
async def buscar_disciplina_por_id(id: str):
    disciplina = await disciplina_repo.get_by_id(id)
    if disciplina:
        return disciplina
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Disciplina com ID {id} não encontrada")

@router.put("/{id}", response_model=DisciplinaModel)
async def atualizar_disciplina(id: str, disciplina_update: UpdateDisciplinaModel = Body(...)):
    disciplina_atualizada = await disciplina_repo.update(id, disciplina_update)
    if disciplina_atualizada:
        return disciplina_atualizada
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Disciplina com ID {id} não encontrada")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_disciplina(id: str):
    deletado = await disciplina_repo.delete(id)
    if not deletado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Disciplina com ID {id} não encontrada")
    return
    