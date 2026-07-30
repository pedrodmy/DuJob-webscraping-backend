from playwright.sync_api import sync_playwright

def buscar_vagas():
    vagas_desejadas = []
    
    with sync_playwright() as p:
        # headless=True faz o robô rodar de forma invisível no servidor
        navegador = p.chromium.launch(headless=True)
        pagina = navegador.new_page()
        
        pagina.set_default_navigation_timeout(60000)
        url = "https://www.vagas.com.br/vagas-de-desenvolvedor"
        
        pagina.goto(url, wait_until="domcontentloaded")
        pagina.wait_for_timeout(5000)
        
        linhas_vagas = pagina.locator("li.vaga").all()
        
        for li in linhas_vagas:
            texto_vaga = li.inner_text().strip()
            iniciar_captura = False
            
            # Filtro do professor para termos de TI
            if 'Desenvolvedor' in texto_vaga or 'Analista' in texto_vaga or 'Estágio' in texto_vaga or 'Júnior' in texto_vaga:
                iniciar_captura = True
                
            if iniciar_captura:
                linhas_detalhes = [linha.strip() for linha in texto_vaga.split("\n") if linha.strip()]
                
                if len(linhas_detalhes) >= 2:
                    cargo = linhas_detalhes[0]
                    empresa = linhas_detalhes[1]
                    
                    # Variáveis dinâmicas iniciadas como None (Nulo)
                    localizacao = None
                    salario = None
                    
                    # Procura padrões de localização e salário nas linhas restantes
                    for linha in linhas_detalhes[2:]:
                        if " / " in linha or "Home Office" in linha or "Remoto" in linha:
                            localizacao = linha
                        elif "R$" in linha:
                            salario = linha
                    
                    # Detalhes fica como texto concatenado ou None caso não exista
                    detalhes = " | ".join(linhas_detalhes[2:]) if len(linhas_detalhes) > 2 else None
                    
                    vagas_desejadas.append({
                        "cargo": cargo,
                        "empresa": empresa,
                        "detalhes": detalhes,
                        "localizacao": localizacao,
                        "salario": salario,
                        "link": url
                    })

        navegador.close()
        
    return vagas_desejadas