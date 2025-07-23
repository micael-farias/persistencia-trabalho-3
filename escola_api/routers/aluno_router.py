from fastapi import APIRouter, Body, status, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from pymongo import ASCENDING, DESCENDING
from models.aluno import AlunoBase, AlunoModel, UpdateAlunoModel
from repositories import aluno_repo
from models.complex_models import BoletimCompletoModel
from helpers.sort_order import SortOrder
from models.complex_models import AlunoComTurmaModel

router = APIRouter()

@router.get("/{id}/detalhes", response_model=AlunoComTurmaModel)
async def buscar_aluno_detalhado(id: str):
    aluno_detalhado = await aluno_repo.get_aluno_com_turma(id)
    if aluno_detalhado:
        return aluno_detalhado
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Aluno com ID {id} não encontrado.")

@router.get("/{id}/boletim", response_model=BoletimCompletoModel)
async def buscar_boletim_aluno(id: str):
    boletim = await aluno_repo.get_boletim_detalhado(id)
    if boletim:
        return boletim
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Aluno com ID {id} não encontrado ou não possui notas.")

@router.get("/count", response_model=dict)
async def contar_alunos():
    total = await aluno_repo.count()
    return {"total_de_alunos": total}

@router.post("/", response_model=AlunoModel, status_code=status.HTTP_201_CREATED)
async def criar_aluno(aluno: AlunoBase = Body(...)):
    return await aluno_repo.create(aluno)

@router.get("/", response_model=List[AlunoModel])
async def listar_alunos(nome: Optional[str] = None, ano_escolar: Optional[int] = None, data_nascimento_inicio: Optional[datetime] = Query(None, description="Data de início (formato ISO: YYYY-MM-DD)"), data_nascimento_fim: Optional[datetime] = Query(None, description="Data de fim (formato ISO: YYYY-MM-DD)"), sort_by: Optional[str] = Query(None, description="Campo para ordenação (ex: nome, data_nascimento)"), sort_order: SortOrder = Query(SortOrder.asc, description="Ordem da ordenação"), page: int = 1, limit: int = 10):
    skip = (page - 1) * limit
    order = DESCENDING if sort_order == SortOrder.desc else ASCENDING
    return await aluno_repo.search(nome=nome, ano_escolar=ano_escolar, data_nascimento_inicio=data_nascimento_inicio, data_nascimento_fim=data_nascimento_fim, sort_by=sort_by, sort_order=order, skip=skip, limit=limit)

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