from sqlalchemy import Column, Integer, String, Text, Float, Boolean, TIMESTAMP
from sqlalchemy.sql import text
from database import Base

class Noticia(Base):
    __tablename__ = "noticias"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    resumo = Column(Text, nullable=False)
    tempo_publicacao = Column(String(100))
    link = Column(String(500), nullable=False)


class Vaga(Base):
    __tablename__ = "vagas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    empresa = Column(String(255), nullable=False)
    localizacao = Column(String(255))
    salario = Column(String(100))
    descricao = Column(Text)
    link_original = Column(String(500))


class Talento(Base):
    __tablename__ = "talentos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    especialidade = Column(String(255))
    habilidades = Column(Text)
    avaliacao = Column(Float)
    preco_hora = Column(Float)