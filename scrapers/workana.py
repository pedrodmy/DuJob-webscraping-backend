import requests
import re

URL = "https://www.workana.com/pt/freelancers"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://www.workana.com/pt/freelancers"
}

def converter_preco(valor):
    if not valor: 
        return None

    numeros = re.sub(r"[^\d,]", "", str(valor))
    numeros = numeros.replace(",", ".")

    try: 
        return float(numeros)
    except ValueError: 
        return None

def buscar_talentos(max_pages=3):
    talentos = []
    
    for page in range(1, max_pages + 1):
        try:
            resposta = requests.get(
                URL,
                headers=HEADERS,
                params={"page": page},
                timeout=10
            )
            resposta.raise_for_status()
            
            dados = resposta.json()
            resultados = dados.get("results", {}).get("results", [])
            
            if not resultados: 
                break

            for perfil in resultados:
                nome = perfil.get("profileName")
                if not nome:
                    continue

                # 🔹 Tratamento correto para o link do perfil
                url_original = perfil.get("profileUrl")
                if url_original:
                    # Se já começa com http, usa direto. Se começa com /, completa o domínio.
                    if url_original.startswith("http"):
                        link_perfil = url_original
                    elif url_original.startswith("/"):
                        link_perfil = f"https://www.workana.com{url_original}"
                    else:
                        link_perfil = f"https://www.workana.com/{url_original}"
                else:
                    link_perfil = "https://www.workana.com/pt/freelancers"

                habilidades_lista = [s.get("anchorText", "") for s in perfil.get("workerSkills", [])]
                habilidades_str = ", ".join(habilidades_lista) if habilidades_lista else None

                talentos.append({
                    "nome": nome,
                    "especialidade": perfil.get("roleName"),
                    "habilidades": habilidades_str,
                    "avaliacao": perfil.get("rating"),
                    "preco_hora": converter_preco(perfil.get("hourlyRate")),
                    "link": link_perfil
                })
        except Exception as e:
            print(f"Erro ao buscar talentos na página {page}: {e}")
            break
            
    return talentos