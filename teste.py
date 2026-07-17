from database import sessionLocal
import crud
from scrapers.workana import buscar_talentos

db = sessionLocal()

talentos = buscar_talentos()

crud.salvar_talentos_no_banco(talentos, db)

print(f"{len(talentos)} talentos salvos!")