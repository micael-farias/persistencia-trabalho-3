from .aluno_repository import AlunoRepository
from .professor_repository import ProfessorRepository
from .disciplina_repository import DisciplinaRepository
from .turma_repository import TurmaRepository
from .nota_repository import NotaRepository

aluno_repo = AlunoRepository()
professor_repo = ProfessorRepository()
disciplina_repo = DisciplinaRepository()
turma_repo = TurmaRepository()
nota_repo = NotaRepository()