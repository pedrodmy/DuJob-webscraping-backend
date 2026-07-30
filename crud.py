from sqlalchemy.orm import Session
import models
import schemas

def salvar_noticias_no_banco(lista_de_noticias_extraidas, db: Session):
    for noticia in reversed(lista_de_noticias_extraidas):
        noticia_validada = schemas.NoticiaBase(**noticia)

        noticia_existente = db.query(models.Noticia).filter(models.Noticia.link == noticia_validada.link).first()

        if not noticia_existente:
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
    busca_completa_de_noticias = db.query(models.Noticia).order_by(models.Noticia.id.desc()).limit(12).all()
    
    return busca_completa_de_noticias

def salvar_talentos_no_banco(lista_de_talentos, db: Session):
    for talento in lista_de_talentos:
        talento_validado = schemas.TalentoBase(**talento)

        # Verifica se o talento já existe pelo nome
        talento_existente = db.query(models.Talento).filter(models.Talento.nome == talento_validado.nome).first()

        if talento_existente:
            # 🔹 Se já existe, atualiza os dados e o link correto
            talento_existente.especialidade = talento_validado.especialidade
            talento_existente.habilidades = talento_validado.habilidades
            talento_existente.avaliacao = talento_validado.avaliacao
            talento_existente.preco_hora = talento_validado.preco_hora
            talento_existente.link = talento_validado.link
        else:
            # 🔹 Se não existe, cria um novo incluindo o link
            novo_talento = models.Talento(
                nome=talento_validado.nome,
                especialidade=talento_validado.especialidade,
                habilidades=talento_validado.habilidades,
                avaliacao=talento_validado.avaliacao,
                preco_hora=talento_validado.preco_hora,
                link=talento_validado.link
            )
            db.add(novo_talento)
            
    db.commit()

def buscar_talentos(db: Session):
    return db.query(models.Talento).all()


def salvar_vagas_no_banco(lista_de_vagas_extraidas, db: Session):
    for vaga in lista_de_vagas_extraidas:
        
        # 🔹 Agora pegamos exatamente o que o robô extraiu.
        # Se ele não achou (ex: salario), o .get() retorna None (Nulo) automaticamente.
        dados_vaga = {
            "titulo": vaga.get("cargo"),
            "empresa": vaga.get("empresa"),
            "descricao": vaga.get("detalhes"),
            "localizacao": vaga.get("localizacao"),
            "salario": vaga.get("salario"),
            "link_original": vaga.get("link")
        }
        
        vaga_validada = schemas.VagaBase(**dados_vaga)

        vaga_existente = db.query(models.Vaga).filter(
            models.Vaga.titulo == vaga_validada.titulo,
            models.Vaga.empresa == vaga_validada.empresa
        ).first()

        if not vaga_existente:
            nova_vaga_db = models.Vaga(
                titulo=vaga_validada.titulo,
                empresa=vaga_validada.empresa,
                localizacao=vaga_validada.localizacao,
                salario=vaga_validada.salario,
                descricao=vaga_validada.descricao,
                link_original=vaga_validada.link_original
            )
            db.add(nova_vaga_db)
            
    db.commit()

def buscar_vagas(db: Session):
    # Busca as últimas 20 vagas no banco de dados
    busca_completa_de_vagas = db.query(models.Vaga).order_by(models.Vaga.id.desc()).limit(20).all()
    return busca_completa_de_vagas