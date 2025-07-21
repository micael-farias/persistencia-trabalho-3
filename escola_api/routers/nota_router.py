from fastapi import APIRouter, Body, status, HTTPException
from models.nota import NotaBase, NotaModel
from repositories import nota_repo

router = APIRouter()

@router.post(
    "/",
    response_description="Lançar nova nota",
    response_model=NotaModel,
    status_code=status.HTTP_201_CREATED
)
async def criar_nota(nota: NotaBase = Body(...)):
    return await nota_repo.create(nota)

@router.get(
    "/{id}",
    response_description="Buscar nota por ID",
    response_model=NotaModel
)
async def buscar_nota_por_id(id: str):
    nota = await nota_repo.get_by_id(id)
    if nota:
        return nota
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Nota com ID {id} não encontrada")