from fastapi import APIRouter, Body, status, HTTPException
from typing import List, Optional
from models.professor import ProfessorBase, ProfessorModel, UpdateProfessorModel
from repositories import professor_repo
from models.complex_models import DesempenhoProfessorModel

router = APIRouter()

@router.get("/{id}/desempenho", response_model=DesempenhoProfessorModel)
async def buscar_desempenho_professor(id: str):
    desempenho = await professor_repo.get_desempenho_por_disciplina(id)
    if desempenho:
        return desempenho
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Professor com ID {id} não encontrado.")

@router.get("/count", response_model=dict)
async def contar_professores():
    total = await professor_repo.count()
    return {"total_de_professores": total}

@router.post("/", response_model=ProfessorModel, status_code=status.HTTP_201_CREATED)
async def criar_professor(professor: ProfessorBase = Body(...)):
    return await professor_repo.create(professor)

@router.get("/", response_model=List[ProfessorModel])
async def listar_professores(nome: Optional[str] = None, email: Optional[str] = None, telefone: Optional[str] = None, departamento: Optional[str] = None, page: int = 1, limit: int = 10):
    skip = (page - 1) * limit
    return await professor_repo.search(nome=nome, email=email, telefone=telefone, departamento=departamento, skip=skip, limit=limit)

@router.get("/{id}", response_model=ProfessorModel)
async def buscar_professor_por_id(id: str):
    professor = await professor_repo.get_by_id(id)
    if professor:
        return professor
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Professor com ID {id} não encontrado")

@router.put("/{id}", response_model=ProfessorModel)
async def atualizar_professor(id: str, professor_update: UpdateProfessorModel = Body(...)):
    professor_atualizado = await professor_repo.update(id, professor_update)
    if professor_atualizado:
        return professor_atualizado
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Professor com ID {id} não encontrado")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_professor(id: str):
    deletado = await professor_repo.delete(id)
    if not deletado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Professor com ID {id} não encontrado")
    return
