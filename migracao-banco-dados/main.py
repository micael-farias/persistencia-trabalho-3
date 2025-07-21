from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from models import User, SessionLocal, init_db
from migrate import migrate_data  # supondo que a função esteja num arquivo migrate_script.py

app = FastAPI()

# Inicializa o banco de dados
init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/")
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(User).offset(skip).limit(limit).all()

@app.post("/users/")
def create_user(name: str, email: str, age: int, db: Session = Depends(get_db)):
    user = User(name=name, email=email, age=age)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.post("/migrate/")
def run_migration():
    migrate_data()
    return {"message": "Migração concluída com sucesso"}
