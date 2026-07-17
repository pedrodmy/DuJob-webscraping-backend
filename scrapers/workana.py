import requests
import re

URL = "https://www.workana.com/pt/freelancers"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "X-Requested-With": "XMLHttpRequest"
}

def converter_preco(valor):
    if not valor: return 0.0

    numeros = re.sub(r"[^\d,]", "", str(valor))
    numeros = numeros.replace(",", ".")

    try: return float(numeros)
    except ValueError: return 0.0

def buscar_talentos(max_pages=3):
    talentos = []
    for page in range(1, max_pages + 1):
        resposta = requests.get(
            URL,
            headers=HEADERS,
            params={"page": page}
        )
        resposta.raise_for_status()
        resultados = resposta.json()["results"]["results"]
        if not resultados: break

        for perfil in resultados:
            talentos.append({
                "nome": perfil.get("profileName"),
                "especialidade": perfil.get("roleName"),
                "habilidades": ", ".join(
                    s["anchorText"] for s in perfil.get("workerSkills", [])
                ),
                "avaliacao": perfil.get("rating") or 0,
                "preco_hora": converter_preco(
                    perfil.get("hourlyRate")
                )
            })
    return talentos