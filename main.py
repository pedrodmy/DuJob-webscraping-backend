from fastapi import FastAPI, status, Depends
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.params import Body 
import schemas
import models
from database import engine, get_db, sessionLocal
from sqlalchemy.orm import Session
from typing import List
from scrapers.scraper_g1 import raspar_noticias_g1
from scrapers.workana import buscar_talentos
import crud
from apscheduler.schedulers.background import BackgroundScheduler

models.Base.metadata.create_all(bind=engine)

app = FastAPI ()
origins = [
    'http://localhost:3000'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

def rodar_robo_automaticamente():
    print("⏰ [Automático] Iniciando coleta de notícias do G1...")
    db = sessionLocal()
    try:
        noticias_extraidas = raspar_noticias_g1()
        crud.salvar_noticias_no_banco(noticias_extraidas, db)
        print("✅ [Automático] Notícias atualizadas com sucesso no banco!")
    finally:
        db.close()

scheduler = BackgroundScheduler()
scheduler.add_job(rodar_robo_automaticamente, 'interval', minutes=30) 
scheduler.start()

@app.get("/")
async def root():
    return{"message": "Hello World"}

@app.get("/api/noticias")
def listar_noticias(db: Session = Depends(get_db)):
    noticias_encontradas = crud.buscar_noticias(db)
    return noticias_encontradas

@app.get("/vagas")
def listar_vagas():
    return []

@app.get("/talentos")
def listar_talentos(db: Session = Depends(get_db)):
    return crud.buscar_talentos(db)

@app.post("/talentos/atualizar")
def atualizar_talentos(db: Session = Depends(get_db)):
    dados = buscar_talentos()
    crud.salvar_talentos_no_banco(dados, db)

    return {"mensagem": "Talentos atualizados"}

@app.post("/api/scraper/run")
def disparar_scraper(db: Session = Depends(get_db)):
    noticias_extraidas = raspar_noticias_g1()
    crud.salvar_noticias_no_banco(noticias_extraidas, db)

    return{"mensagem": "Sucesso!"}