from fastapi import FastAPI, status, Depends
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.params import Body 
import schemas
import models
from database import engine, get_db
from sqlalchemy.orm import Session
from typing import List
from scrapers.scraper_g1 import raspar_noticias_g1
import crud

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
def listar_talentos():
    return []