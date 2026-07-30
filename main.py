from fastapi import FastAPI, status, Depends
from fastapi.middleware.cors import CORSMiddleware
import schemas
import models
from database import engine, get_db, sessionLocal
from sqlalchemy.orm import Session
from typing import List
from scrapers.scraper_g1 import raspar_noticias_g1
from scrapers.workana import buscar_talentos
import crud
from apscheduler.schedulers.background import BackgroundScheduler
from scrapers.vagas import buscar_vagas as raspar_vagas_playwright
import threading

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

# 🔹 Função unificada que roda todos os scrapers com segurança
def rodar_todos_os_scrapers():
    print("🤖 [Automático] Iniciando a coleta de todos os robôs (Notícias, Talentos e Vagas)...")
    db = sessionLocal()
    try:
        # 1. Raspar Notícias do G1
        try:
            print("📰 [Robô G1] Buscando notícias...")
            noticias_extraidas = raspar_noticias_g1()
            crud.salvar_noticias_no_banco(noticias_extraidas, db)
            print("✅ [Robô G1] Notícias salvas com sucesso!")
        except Exception as e:
            print(f"❌ Erro no robô do G1: {e}")

        # 2. Raspar Talentos (Workana)
        try:
            print("👥 [Robô Talentos] Buscando profissionais...")
            dados_talentos = buscar_talentos()
            crud.salvar_talentos_no_banco(dados_talentos, db)
            print("✅ [Robô Talentos] Talentos salvos com sucesso!")
        except Exception as e:
            print(f"❌ Erro no robô de talentos: {e}")

        # 3. Raspar Vagas (Playwright)
        try:
            print("💼 [Robô Vagas] Buscando vagas...")
            dados_vagas = raspar_vagas_playwright()
            crud.salvar_vagas_no_banco(dados_vagas, db)
            print(f"✅ [Robô Vagas] {len(dados_vagas)} vagas salvas com sucesso!")
        except Exception as e:
            print(f"❌ Erro no robô de vagas: {e}")

        print("🎉 [Automático] Processo de coleta completo finalizado!")
    finally:
        db.close()

# 🔹 Dispara todos os robôs automaticamente assim que o servidor FastAPI é aberto
@app.on_event("startup")
def iniciar_servidor():
    print("🚀 Servidor FastAPI iniciado. Acionando robôs em segundo plano...")
    thread = threading.Thread(target=rodar_todos_os_scrapers)
    thread.daemon = True
    thread.start()

# 🔹 Mantém o agendamento rodando a cada 30 minutos (opcional, continua atualizando sozinho)
scheduler = BackgroundScheduler()
scheduler.add_job(rodar_todos_os_scrapers, 'interval', minutes=30) 
scheduler.start()

@app.get("/")
async def root():
    return{"message": "Hello World"}

@app.get("/api/noticias")
def listar_noticias(db: Session = Depends(get_db)):
    noticias_encontradas = crud.buscar_noticias(db)
    return noticias_encontradas

@app.get("/api/talentos")
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

@app.post("/vagas/atualizar")
def atualizar_vagas(db: Session = Depends(get_db)):
    try:
        dados = raspar_vagas_playwright()
        crud.salvar_vagas_no_banco(dados, db) 
        return {"mensagem": f"{len(dados)} vagas atualizadas com sucesso!"}
    except Exception as e:
        print(f"❌ Erro ao atualizar vagas: {e}")
        return {"erro": str(e)}

@app.get("/api/vagas")
def listar_vagas(db: Session = Depends(get_db)):
    return crud.buscar_vagas(db)

@app.get("/api/indicadores")
def obter_indicadores(db: Session = Depends(get_db)):
    total_vagas = db.query(models.Vaga).count()
    total_talentos = db.query(models.Talento).count()
    total_noticias = db.query(models.Noticia).count()

    return {
        "total_vagas": total_vagas,
        "total_talentos": total_talentos,
        "total_noticias": total_noticias
    }