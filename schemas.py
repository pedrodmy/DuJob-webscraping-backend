from pydantic import BaseModel 
from typing import Optional

class NoticiaBase(BaseModel):
    titulo: str
    resumo: str
    tempo_publicacao: str
    link: str
    secao_de_publicacao: str
    imagem_da_noticia: str
class NoticiaCreate(NoticiaBase): pass
class Noticia(NoticiaBase):
    id: int
    class Config:
        from_attributes = True


class VagaBase(BaseModel):
    titulo: str
    empresa: str
    localizacao: Optional[str] = None # 🔹 Agora aceita Nulo
    salario: Optional[str] = None     # 🔹 Agora aceita Nulo
    descricao: Optional[str] = None
    link_original: Optional[str] = None

class VagaCreate(VagaBase): pass
class Vaga(VagaBase):
    id: int
    class Config:
        from_attributes = True


class TalentoBase(BaseModel):
    nome: str
    especialidade: Optional[str] = None
    habilidades: Optional[str] = None
    avaliacao: Optional[float] = None
    preco_hora: Optional[float] = None
    link: Optional[str] = None

    class Config:
        from_attributes = True