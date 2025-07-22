from fastapi import APIRouter, Body, status, HTTPException
from typing import List, Optional
from models.nota import NotaBase, NotaModel, UpdateNotaModel
from repositories import nota_repo
from models.base import PyObjectId

router = APIRouter()

@router.get("/count", response_model=dict)
async def contar_notas():
    total = await nota_repo.count()
    return {"total_de_notas": total}

@router.post("/", response_model=NotaModel, status_code=status.HTTP_201_CREATED)
async def criar_nota(nota: NotaBase = Body(...)):
    return await nota_repo.create(nota)

@router.get("/", response_model=List[NotaModel])
async def listar_notas(aluno_id: Optional[PyObjectId] = None, disciplina_id: Optional[PyObjectId] = None, nota_min: Optional[float] = None, nota_max: Optional[float] = None, page: int = 1, limit: int = 10):
    skip = (page - 1) * limit
    return await nota_repo.search(aluno_id=aluno_id, disciplina_id=disciplina_id, nota_min=nota_min, nota_max=nota_max, skip=skip, limit=limit)

@router.get("/{id}", response_model=NotaModel)
async def buscar_nota_por_id(id: str):
    nota = await nota_repo.get_by_id(id)
    if nota:
        return nota
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Nota com ID {id} não encontrada")

@router.put("/{id}", response_model=NotaModel)
async def atualizar_nota(id: str, nota_update: UpdateNotaModel = Body(...)):
    nota_atualizada = await nota_repo.update(id, nota_update)
    if nota_atualizada:
        return nota_atualizada
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Nota com ID {id} não encontrada")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_nota(id: str):
    deletado = await nota_repo.delete(id)
    if not deletado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Nota com ID {id} não encontrada")
    return
