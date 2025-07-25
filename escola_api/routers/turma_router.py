from fastapi import APIRouter, Body, status, HTTPException
from typing import List, Optional
from models.turma import TurmaBase, TurmaModel, UpdateTurmaModel
from repositories import turma_repo
from models.complex_models import TurmaComAlunosModel

router = APIRouter()

@router.get("/{id}/detalhes", response_model=TurmaComAlunosModel)
async def buscar_turma_detalhada(id: str):
    turma_detalhada = await turma_repo.get_turma_com_alunos(id)
    if turma_detalhada:
        return turma_detalhada
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Turma com ID {id} não encontrada.")


@router.get("/count", response_model=dict)
async def contar_turmas():
    total = await turma_repo.count()
    return {"total_de_turmas": total}

@router.post("/", response_model=TurmaModel, status_code=status.HTTP_201_CREATED)
async def criar_turma(turma: TurmaBase = Body(...)):
    return await turma_repo.create(turma)

@router.get("/", response_model=List[TurmaModel])
async def listar_turmas(serie_ano: Optional[str] = None, turno: Optional[str] = None, ano_letivo: Optional[int] = None, page: int = 1, limit: int = 10):
    skip = (page - 1) * limit
    return await turma_repo.search(serie_ano=serie_ano, turno=turno, ano_letivo=ano_letivo, skip=skip, limit=limit)

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