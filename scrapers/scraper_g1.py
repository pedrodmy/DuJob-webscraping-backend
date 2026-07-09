import requests
from bs4 import BeautifulSoup

def raspar_noticias_g1():

    resposta = requests.get('https://g1.globo.com/tecnologia/')

    lista_de_noticias_extraidas = []

    if (resposta.status_code == 200):
        soup = BeautifulSoup(resposta.content, 'html.parser')
        conteudo_noticia = soup.find_all('div', class_='bastian-feed-item')
        
        for noticias in conteudo_noticia:
            conteudo_da_noticia = noticias.find('a', class_='feed-post-link')
            print(conteudo_da_noticia, "\n")

            titulo_noticia_limpo = conteudo_da_noticia.text.strip()
            print("Título:", titulo_noticia_limpo, "\n")

            link_da_noticia = conteudo_da_noticia.get('href')
            print("Link:", link_da_noticia, "\n")

            tempo_de_publicacao = noticias.find('span', class_='feed-post-datetime')
            tempo_limpo = tempo_de_publicacao.text.strip()
            print(tempo_limpo, "\n")

            secao_da_publicacao = noticias.find('span', class_='feed-post-metadata-section')
            secao_limpa = secao_da_publicacao.text.strip()
            print(secao_limpa, "\n")

            imagem_da_publicacao = noticias.find('img', class_='bstn-fd-picture-image')
            if imagem_da_publicacao != None:
                imagem_limpa = imagem_da_publicacao.get('src')
            else:
                imagem_limpa = "Sem imagem"
                
            print("Imagem:", imagem_limpa, "\n")

            resumo_da_noticia = noticias.find('div', class_='feed-post-body-resumo')

            if resumo_da_noticia != None:
                resumo_limpo = resumo_da_noticia.text.strip()
                if titulo_noticia_limpo != resumo_limpo:
                    print("Resumo:", resumo_limpo, "\n")
                else:
                    print("")
            else:
                print("Não possui resumo \n")
                resumo_limpo = "Sem resumo"

            nova_noticia = {
                "titulo": titulo_noticia_limpo,
                "link": link_da_noticia,
                "tempo_de_publicacao": tempo_limpo,
                "secao_de_publicacao": secao_limpa,
                "resumo": resumo_limpo,
                "imagem_da_noticia": imagem_limpa
            }

            lista_de_noticias_extraidas.append(nova_noticia)

    return lista_de_noticias_extraidas
if __name__=="__main__":
    dados = raspar_noticias_g1()
    print(f"Foram raspadas {len(dados)} notícias com sucesso!")
    print(dados[0])