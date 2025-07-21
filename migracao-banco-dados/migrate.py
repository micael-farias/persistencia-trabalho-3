from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Base  

SQLITE_DATABASE_URL = "sqlite:///./test.db"
POSTGRES_DATABASE_URL = "postgresql+psycopg2://meuusuario:minhasenha@localhost/meubanco"

sqlite_engine = create_engine(SQLITE_DATABASE_URL)
SessionSQLite = sessionmaker(bind=sqlite_engine)
postgres_engine = create_engine(POSTGRES_DATABASE_URL)
SessionPostgres = sessionmaker(bind=postgres_engine)

Base.metadata.create_all(bind=postgres_engine)

def migrate_data():
    sqlite_session = SessionSQLite()
    postgres_session = SessionPostgres()

    users = sqlite_session.query(User).all()
    
    for user in users:
        new_user = User(id=user.id, name=user.name, email=user.email)
        postgres_session.add(new_user)
    
    postgres_session.commit()
    sqlite_session.close()
    postgres_session.close()
