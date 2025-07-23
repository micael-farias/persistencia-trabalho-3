# API de Sistema Escolar - FastAPI e MongoDB

## Descrição
API REST para gerenciamento de um sistema escolar, desenvolvida em Python com FastAPI e o banco de dados NoSQL MongoDB. O projeto implementa funcionalidades completas para as entidades da escola, além de recursos avançados como paginação, filtros dinâmicos, ordenação e consultas de agregação complexas.

## Funcionalidades Implementadas

### CRUD Completo (F3)
* **Entidades:** Professor, Aluno, Disciplina, Turma, Nota.
* Operações de Criação, Leitura, Atualização e Deleção para todas as entidades.
* **Autor(es):** Michael Farias

### Contagem de Registros (F4)
* Endpoints `/count` para obter a quantidade total de registros em cada coleção.
* **Autor(es):** Michael Farias

### Paginação e Limitação (F5)
* Parâmetros `page` e `limit` nos endpoints de listagem para controle de paginação.
* **Autor(es):** Ezequiel Melo

### Filtros e Buscas Avançadas (F6)
* Filtros por atributos específicos (ex: `ano_escolar` de um aluno).
* Busca textual parcial (semelhante ao `LIKE`) em campos como `nome` e `ementa`.
* Filtros por intervalo de datas (ex: buscar alunos por data de nascimento).
* **Autor(es):** Ezequiel Melo

### Agregações, Ordenações e Consultas Complexas (F7)
* **Ordenação:** Classificação dos resultados por campos customizáveis (ex: ordenar alunos por nome).
* **Agregações e Contagens:** Métodos para contagem total de documentos.
* **Consultas Complexas:**
  * **Boletim do Aluno:** Rota que busca um aluno e agrega todas as suas notas, com detalhes das disciplinas e dos professores responsáveis (envolvendo 4 coleções).
  * **Desempenho do Professor:** Rota que analisa um professor e calcula a média de notas para cada disciplina que ele leciona (envolvendo 3 coleções).
* **Autor(es):** Ezequiel Melo

### Estrutura do Projeto
* **Arquitetura Modular:** Separação clara de responsabilidades em `models`, `repositories` e `routers`.
* **Padrão Repository:** Lógica de acesso ao banco de dados isolada na camada de repositório.
* **Schemas Pydantic:** Validação de dados de entrada e saída, além da geração automática da documentação.
* **Autor(es):** Michael Farias

### Configuração do Banco de Dados
* Conexão com o MongoDB utilizando a biblioteca assíncrona `motor`.
* Uso de variáveis de ambiente (`.env`) para configuração segura da conexão.
* Suporte para execução do banco de dados via Docker.
* **Autor(es):** Michael Farias

## Como Executar

1. **Clone o repositório**
2. **Crie e ative um ambiente virtual**
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   # venv\Scripts\activate  # Windows

3. **Instale as dependências**
   ```sh
   pip install -r requirements.txt
   ```
4. **Configure o banco de dados**
   - Edite o arquivo `alembic.ini` com a URL do seu banco MySQL
5. **Rode as migrações**
   ```sh
   alembic upgrade head
   ```
6. **Inicie a aplicação**
   ```sh
   uvicorn app.main:app --reload
   ```
7. **Acesse a documentação interativa**
   - http://localhost:8000/docs
