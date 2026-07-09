from fastapi import FastAPI, status, Depends
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.params import Body 
import schemas
import models
from database import engine, getDB
from sqlalchemy.orm import Session
from typing import List

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

@app.get("/noticias")
def listar_noticias():
    return []

@app.get("/vagas")
def listar_vagas():
    return []

@app.get("/talentos")
def listar_talentos():
    return []