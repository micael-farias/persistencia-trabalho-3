from fastapi import FastAPI
from routers import aluno_router, professor_router, disciplina_router, turma_router, nota_router
from logging_config import setup_logging

setup_logging()

app = FastAPI(
    title="API Escola de Ensino Médio",
    description="API para gerenciar uma escola usando FastAPI e MongoDB.",
    version="1.0.0"
)

app.include_router(aluno_router.router, tags=["Alunos"], prefix="/alunos")
app.include_router(professor_router.router, tags=["Professores"], prefix="/professores")
app.include_router(disciplina_router.router, tags=["Disciplinas"], prefix="/disciplinas")
app.include_router(turma_router.router, tags=["Turmas"], prefix="/turmas")
app.include_router(nota_router.router, tags=["Notas"], prefix="/notas")
