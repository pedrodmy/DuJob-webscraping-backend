from sqlalchemy.orm import Session
import models
import schemas

def salvar_noticias_no_banco(lista_de_noticias_extraidas, db: Session):
    for noticia in lista_de_noticias_extraidas:
        noticia_validada = schemas.NoticiaBase(**noticia)

        nova_noticia_db = models.Noticia(
             titulo=noticia_validada.titulo,
             link=noticia_validada.link,
             tempo_publicacao=noticia_validada.tempo_publicacao,
             secao_de_publicacao=noticia_validada.secao_de_publicacao,
             resumo=noticia_validada.resumo,
             imagem_da_noticia=noticia_validada.imagem_da_noticia

        )

        db.add(nova_noticia_db)
    
    db.commit()

def buscar_noticias(db: Session):
    busca_completa_de_noticias = db.query(models.Noticia).all()

    return busca_completa_de_noticias