from pydantic import BaseModel 

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
    localizacao: str
    salario: str
    descricao: str
    link_original: str

class VagaCreate(VagaBase): pass
class Vaga(VagaBase):
    id: int
    class Config:
        from_attributes = True


class TalentoBase(BaseModel):
    nome: str
    especialidade: str
    habilidades: str
    avaliacao: float
    preco_hora: float
class TalentoCreate(TalentoBase): pass
class Talento(TalentoBase):
    id: int
    class Config:
        from_attributes = True