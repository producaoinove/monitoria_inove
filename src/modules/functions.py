from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from selenium import webdriver
import os
import logging
from datetime import datetime


def realizar_login(
    navegador: webdriver.Chrome, ambiente: str, login: str, senha: str
) -> webdriver.Chrome:
    """
    Realiza o login na Nossa URA

    Entrada:
        navegador(webdriver.Chrome): recebe um navegador ativo que seja comandado pelo mesmo.
        ambiente (str): url para fazer login
        login (str): login
        senha (str): senha

    Saída:
        O navegador com instância ativa do Nossa URA
    """

    from settings import path_log
    import os
    import time

    realizar_login = os.path.join(path_log, "login.png")

    try:
        navegador.get(ambiente)
        time.sleep(10)
        navegador.save_screenshot(realizar_login)

        username = navegador.find_element(By.NAME, "email")
        password = navegador.find_element(By.NAME, "password")

        if username.is_displayed() and password.is_displayed():
            username.send_keys(str(login))
            password.send_keys(str(senha))

        login_button = navegador.find_element(
            By.CSS_SELECTOR, "button.btn.btn-block.btn-flat.btn-primary"
        )
        if login_button.is_displayed():
            login_button.click()

        wait = WebDriverWait(navegador, 10)
        elemento_carregado = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.content-header"))
        )
        if "Dashboard" in elemento_carregado.text:
            pass
        else:
            raise Exception("Impossivel logar na Nossa URA")

        return navegador
    except Exception as e:
        raise Exception(f"Impossivel logar na Nossa URA, detalhes: {str(e)}")


def ir_campanha(navegador: webdriver.Chrome, campanha: str) -> webdriver.Chrome:
    """
    Realiza ida para parte de campanhas

    Entrada:
        navegador(webdriver.Chrome): recebe um navegador ativo que seja comandado pelo mesmo.
        campanha (str): caminho ida para campanhas

    Saída:
        O navegador com instância ativa do Nossa URA em CAMPANHAS
    """

    import os
    from settings import path_log

    campanha_lugar = os.path.join(path_log, "campanha.png")

    try:

        import time

        time.sleep(30)

        navegador.get(campanha)

        wait = WebDriverWait(navegador, 60)
        element = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//td[contains(@class, "text-center")]')
            )
        )

        import time

        time.sleep(30)

        if element:
            navegador.save_screenshot(campanha_lugar)
        else:
            raise Exception("Impossivel ir para CAMPANHAS")

        return navegador
    except Exception as e:
        raise Exception(f"Impossivel ir para CAMPANHAS, detalhes: {str(e)}")


def extracao_campanha_nossaura(navegador: webdriver.Chrome) -> tuple:
    """
    Realiza a extração dos dados necessários e coloca em uma tupla que contém os dados necessários para realizar o calculo do tempo de discagem.

    Entrada:
        navegador (webdriver.Chrome) -> navegador iterável para realizar coleta dos dados da discagem

    Saída:
        tupla com dados que estão no site
    """

    tabela = navegador.find_element(By.XPATH, "//table")
    resultado = []
    lista_filas = []
    linhas = tabela.find_elements(By.XPATH, ".//tr")

    for linha in linhas[1:]:
        colunas = linha.find_elements(By.XPATH, ".//td")
        if len(colunas) >= 3:
            nome = colunas[0].text.strip()
            contato = colunas[1].text.strip()
            canais = int(colunas[2].text.strip())
            print(nome, contato, canais)
            if "_" in nome:
                nome.replace("_", "-")
            if "TESTE" not in str(nome).upper():
                prefixo = nome.split("-")[0] + nome.split("-")[1]
                print(prefixo)
                if prefixo not in lista_filas:
                    contatos = contato.split("/")
                    utilizados = contatos[0].replace(" utilizados ", "")
                    utilizados = int(utilizados)
                    total = contatos[1].replace(" Total: ", "")
                    total = int(total)
                    lista_filas.append(prefixo)
                else:
                    novos_contatos = contato.split("/")
                    n_utilizados = novos_contatos[0].replace(" utilizados ", "")
                    utilizados = int(n_utilizados) + utilizados
                    n_total = novos_contatos[1].replace(" Total: ", "")
                    total = int(n_total) + total
                auxiliar = (nome, utilizados, total, canais)
                resultado.append(auxiliar)
    return resultado


def tratar_dados_campanha(dados_extraidos: tuple) -> tuple:
    """
    Trata os dados da campanha, deixando da forma que o bot precisa para analisar

    Entrada:
        dados_extraidos (tuple): tupla de dados retirados do site da Nossa URA

    Saída:
        Uma tupla de tuplas com dados da campanha: primeiro elemento é nome da fila (nenhum tratamento), segundo elemento é a quantidade de Contatos utilizados (precisa ser inteiro), terceiro elemento é a quantidade de Contatos Total (precisa ser inteiro), quarto elemento é a quantidade de Canais (precisa ser inteiro)
    """

    dados_tratados = []

    for item in dados_extraidos:
        nome_fila = item[0]
        contatos_utilizados = int(item[1])
        contatos_total = int(item[2])
        canais = int(item[3])

        dados_tratados.append((nome_fila, contatos_utilizados, contatos_total, canais))

    return tuple(dados_tratados)


def pegar_timestamp() -> tuple:
    """
    Coloca o dia de hoje em uma tupla de timestamps.

    Entrada:
        Nenhuma.

    Saída:
        Uma tupla de dois elementos, sendo o primeiro o timestamp do início do dia de hoje e o segundo o timestamp do fim do dia de hoje.
    """

    from datetime import datetime, time, timedelta

    hoje = datetime.now().date()
    # hoje = (datetime.now().date() - timedelta(days=1))
    inicio_dia = int(datetime.combine(hoje, time.min).timestamp())
    fim_dia = int(datetime.combine(hoje, time.max).timestamp())
    return (inicio_dia, fim_dia)


def pegar_id_fila_monitorialeads(fila: str) -> str:
    """

    Coleta o ID da fila a partir do nome da fila.

    Entrada:
        fila: str -> Nome da fila a ser monitorada.

    Saída:
        str -> ID da fila a ser monitorada.

    """

    from settings import filas_monitorar

    if fila in filas_monitorar:
        return filas_monitorar[fila]
    else:
        raise Exception("ID da fila nao encontrado")


def construir_url_monitorialeads(
    ambiente_ipbox: str, fila_analise: str, dia_inicio: str, dia_fim: str
) -> str:
    """
    Constroi a URL para acessar o relatório de chamadas de uma fila.

    Entrada:
        ambiente_ipbox: str -> Ambiente do IPBOX
        fila_analise: str -> ID da fila a ser analisada.
        dia_inicio: str -> Data de início da análise.
        dia_fim: str -> Data de fim da análise.

    Saída:
        str -> URL para acessar o relatório de chamadas da fila analisada.
    """

    url = f"{ambiente_ipbox}viewRelatHistChamadas.php?fila={fila_analise}&de={dia_inicio}&ate={dia_fim}"
    return url


def formatar_data_hora(dt: datetime) -> str:
    """
    Formatar a data e hora para o padrão brasileiro.

    Entrada:
        dt: datetime -> Data e hora a ser formatada.

    Saída:
        str -> Data e hora formatada no padrão brasileiro.
    """

    return dt.strftime("%d/%m/%Y %H:%M")


def extrair_dados_monitorialeads(url: str) -> tuple:
    """
    Extrai os dados do relatório.

    Entrada:
        url: str -> URL do relatório.

    Saída:
        tuple -> Tupla contendo o carimbo de data/hora e o número de telefone
    """

    import requests
    from bs4 import BeautifulSoup
    from datetime import datetime

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Erro ao acessar a página: {response.status_code}")

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table")

    if not table or "não retornou registros" in table.text:
        raise Exception("Ainda nao foram registradas chamadas para a fila analisada")

    linha_analise = table.find_all("tr")[-3]
    carimbo_data_hora = None
    numero_lead = None
    colunas = linha_analise.find_all("td")

    if len(colunas) >= 2:

        carimbo_data_hora_texto = colunas[0].text.strip()
        numero_lead_texto = colunas[1].text.strip()

        try:
            carimbo_data_hora = datetime.strptime(
                carimbo_data_hora_texto, "%d/%m/%Y %H:%M"
            )
            carimbo = formatar_data_hora(carimbo_data_hora)
        except ValueError:
            raise Exception(
                f"Formato de data e hora invalido: {carimbo_data_hora_texto}"
            )

        try:
            numero_lead = numero_lead_texto
            numero_lead = str(numero_lead).replace("-", "")
        except ValueError:
            raise Exception(
                f"Formato de numero de telefone invalido: {numero_lead_texto}"
            )

    return (carimbo, numero_lead)


def extracao_monitorialeads(path_file: str, carimbo: str, numero: str) -> bool:
    """
    Verifica a extração dos dados do relatório e atualiza os arquivos bases da aplicação.

    Entrada:
        path_file: str -> O arquivo base da aplicação
        carimbo: str -> Carimbo de data/hora do último registro extraído.
        numero: str -> Telefone do último registro extraído.

    Saída:
        bool -> True se a extração trouxe uma novidade, False caso contrário.
    """

    import os
    import pandas as pd

    data_dict = {"DATA": [carimbo], "TELEFONE": [numero]}

    if os.path.exists(path_file):
        df = pd.read_csv(path_file, dtype=str)
        telefones_df = df["TELEFONE"].to_list()
        if numero in telefones_df:
            return False
        else:
            nova_linha = pd.DataFrame({"DATA": [carimbo], "TELEFONE": [numero]})
            df = pd.concat([df, nova_linha], ignore_index=True)
            # df.to_csv(path_file, index=False)
            return True
    else:
        df = pd.DataFrame(data_dict)
        # df.to_csv(path_file, index=False)
        return True


def logar_no_whatsapp(
    navegador: webdriver.Chrome, logging: logging.Logger
) -> webdriver.Chrome:

    from settings import setup_log, path_log

    logging.info(setup_log("monitorar", path_log))

    try:
        navegador.get("https://web.whatsapp.com/")

        str(input("Pressione Enter apos logar no wpp..."))

    except Exception as e:
        logging.error(f"Erro ao tentar fazer login no WhatsApp Web: {str(e)}")

    return navegador


def enviar_mensagem(
    navegador: webdriver.Chrome,
    tipo: str,
    destino: str,
    mensagem: str,
    logging: logging.Logger,
) -> str:

    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    import time

    try:
        if tipo not in ["grupo", "privado"]:
            return "Tipo inválido. Use 'grupo' ou 'privado'."

        if tipo == "privado":
            url = f"https://web.whatsapp.com/send?phone={destino}"
        elif tipo == "grupo":
            url = f"https://web.whatsapp.com/accept?code={destino}"

        navegador.get(url)
        campo_mensagem_xpath = '//div[@contenteditable="true"][@data-tab="10"]'
        WebDriverWait(navegador, 20).until(
            EC.element_to_be_clickable((By.XPATH, campo_mensagem_xpath))
        )
        campo_mensagem = navegador.find_element(By.XPATH, campo_mensagem_xpath)
        campo_mensagem.click()
        campo_mensagem.send_keys(mensagem)
        campo_mensagem.send_keys(Keys.ENTER)
        time.sleep(3)
        return "Mensagem enviada com sucesso!"

    except Exception as e:
        return f"Erro ao enviar a mensagem: {str(e)}"


def post_acompanhamento(
    ambiente: str,
    fila: str,
    ultimo_mailing: str,
    tempo_operacao: str,
    criticidade: str,
    canais: str,
    qtd_total: str,
    qtd_trabalhada: str,
) -> json:

    import requests

    api_url = "http://168.121.7.194:5001/api/acompanhamento_mailing_insert"
    header = {
        "username": "producao.inove",
        "password": "Produc@0",
        "token": r"bhi!!cxrJjzP!-x2L29Jw65AHXMGX7l9pOFg3vAAW6e!n?WhFNWDZd=/1U=L!E?68=0lhV3?UKT6mbCrGrpD?xVH0YOX2-0=3n7GR3o=3Iiep6t6oseWI7Yidhs?HIQ2rIfKC3S?6je1M6nN45RK6M?0bhobg4HhJNbq14zGJ7ILx9g2/9cYVPz8ubWDwukVll5P0ZPlAoJVCtftk4Lj?qHJcqoXMfSe8W2bL=7xFLiLNx1-9f-UeV6SEARp7eZl=yM8RpRUq1-zmT-QV0UWPA0ixwe7LKo4XiNY!BlvaLo=KgGvQJIayMJdyRnRt/h=4SA31CsKFYSGXCSpKijefg!TJRNcP8eU!2a9Uqrx1TkaBSKKXPthDcdUSOdy05rhggmye/jGg8TJ!f?a-whYPdN2gXh-JmBg9XfUQ5be4Nj29NowbkD74h0OZaXKBYfpy9E71ayAPXeQOli=z9B9wxvPRIf9VOniR3CaQ?4NzH-l-JSuLT3TOb?WPaI?FBmqj09caxqCMYb/CnfeXRVL2RhW5K1R7ofUR7tjX/V3LAiKC!T?Kv=rZd6g2VxVZ48LQ!RYA4RE=GvcjDiVFJ=7RCZCXsFSsil1sRfL6=lrvB9zKXHuqIIfRZckLz=UMFlvKG!YO677S!X4tluQS/Dmts0YqaqtNHHTr?hLaRww?!/z20lBik7aNqFtsUwFLFDek=l8efmIXyI90A15U2RuRrzURi0P6bAWYGgg/lPZbHN2PoZlAAdtNJT/3G9F6!WFLxoK!6UQm5Lo7LLHlKJo8zvarZISQEmWB=LAhTKFYhiNNaw-pdqkJq5czIwiFfNPBPU6qamSYM3C7a7LEzdZrmAB5F2OrmzQClqE922kcpfqO/0rUu-O=av=FizbQdFK?gC9tqyuF3h80Sb/tf=C5!Oa5sfqmMepQBn4vDnau-iK3Fi3qIKi612dE2yLnbJ4tDG7q0oRgezAfeYAwE=?1T23F2mu-q1rst1TsbPJP7!y8aS7lEQxPpyYwxEuaqp9WOyW9PxMg-8J/TfwuFtmh=4nPOBtamumY1LQ!32UZSkUSJWNOYIVxtaLTXKztwZi7mz=dD5io1qogl8!EHnz047kc0H3EVayUADap7672X6EOVlmXApOziDP?LgPyWcvET8k/BMoJRojVwkbkDwFK=AEBhxNolCamgwmwk1KtfwU/9t11nJzlJYbWzfXxv6nAjQ7mCXngXhPW/!aL4bMj9U?1J5OCzH?UYQ77SI5RCBbgQsgdX1tQ6sBIp8AnFI?!2kIe/X2zX9c0YFnyN3bS7!fvN!=YMNkiwrE5tn6Ql6CKV0bzI5RQBfw!UCfoWUZvyPC-uf38UsGXAMx71ocQm8XPWP05tab7SsaFvPAg/Vh/2J/YyFjAkX9Ec1dsXsJK1LyuahOGphGe6!Ut5RI-l1dpUCe/xKYn=YlO7Z5wkou6YuFKkFY?aWo5?EpZempDPbe-yHv!6o-P-0QVjejO4K9sEnS-muWHLKmVu2!VAweKnv!XVCvgh7yq95/0aryahsXyt8umiPGwYX/lzdtk4w2dDr8Ul6/dSYadYrblVXZ=sm0GMPB9RhZpDx8nKFyF5/D6g/X6FIuSz25SIv7edBatAihp=o-IO/dZIWdzsY4yZNxQOC-m02r?wC?mImr4jMDLcNBgx!m2UAV8aSAFvqJvufA4usCb35S-xADJ8rz25yG-mZkss3UcjApO!9ghrC0XV2Dh18ArdGNzPKJIBdkqcgYNHRrX3SCAzfErqeLz39qMnlitRP!gTnzSO1?VAqr0kwR7OXvzDwzl/hm1l=NP449GDEUKmyx!w2YErmeqXkHXVS9t?HaB?81cH9Qj466g2GBUtZo?-lX1JV38AWg7OmmBIBkoMyvM24td=5?goM60do0DJ61cx/ah9O1hzgHG/8jTvDcxT2sNgkxQMTSNVpruYjIfFV1W1nXJ94ZyctCM3W1ldnkmS=Vv-t6wGHt79jZp=rn7ekUhE6L271dC93TUrs/Xf6u58mD68RiFxVyqU=MqG7qGPSpNAHE",
    }
    payload = {
        "ambiente": ambiente,
        "fila": fila,
        "ultimo_mailing": ultimo_mailing,
        "tempo_operacao": tempo_operacao,
        "criticidade_operacao": criticidade,
        "canais": canais,
        "total_registros": qtd_total,
        "consumo_registros": qtd_trabalhada,
    }
    response = requests.post(api_url, headers=header, json=payload)

    if response.status_code == 200:
        return response.json()
    else:
        return None


def verifica_tempo_operacao(
    registro_total: int, registro_consumido: int, canais: int, operacao: str = ""
) -> str:
    """
    Realiza o calculo de tempo de operacao e informa se a operacao vai ou nao durar nos proximos 30 minutos ( tempo = registros / 70 * canais ) .

    Args:
        registro_total (int): inteiro representando o número de registros total
        registro_consumido (int): inteiro representando o número de registros consumidos
        canais (int): inteiro representando quantidade de canais
        opercao (str): representando qual ambiente de analise é

    Returns:
        string representando 'vai durar' caso o valor de T for maior que 0.5 ou 'nao vai durar' caso seja menor ou igual a 0.5
    """

    if operacao not in ["NOSSA URA", "IPBOX", "IPBOX2", "VONIX"]:
        raise Exception("Opa... Operacao invalida")
    elif operacao == "NOSSA URA":
        valor_operacao = 54
    elif operacao == "IPBOX":
        valor_operacao = 75
    elif operacao == "VONIX":
        valor_operacao = 80

    if canais == 0:
        canais = 1

    try:
        meio_registros = registro_total // 2
        if registro_consumido <= meio_registros:
            criticidade = "vai durar"
            registros = registro_total - registro_consumido
        else:
            registros = registro_total - registro_consumido

        if registros < 0:
            registros *= -1

    except Exception as e:
        raise Exception(
            f"Opa... Os registros foram passados errados, registro_total precisa ser maior do que registro_consumido, {str(e)}"
        )

    try:
        tempo_operacao = registros / (valor_operacao * canais)
        tempo_operacao = round(tempo_operacao, 2)
        horas = int(tempo_operacao)
        minutos = int((tempo_operacao - horas) * 100)
        if minutos >= 60:
            horas += 1
            minutos -= 60
        else:
            horas = horas
            minutos = minutos
        tempo_operacao = float(f"{horas}.{str(minutos).zfill(2)}")
    except Exception as e:
        raise Exception(f"Opa... Erro ao realizar o calculo, {str(e)}")

    tempo_operacao = round(tempo_operacao, 2)
    if tempo_operacao > 1:
        return ("vai durar", tempo_operacao)
    elif 0.5 <= tempo_operacao <= 1:
        return ("subir", tempo_operacao)
    else:
        try:
            return (criticidade, tempo_operacao)
        except:
            return ("nao vai durar", tempo_operacao)


def realizar_login_ipbox(
    navegador: webdriver.Chrome,
    ambiente: str,
    login: str,
    senha: str,
    path_log: str,
    tipo: str,
) -> webdriver.Chrome:
    """
    Realiza o login no ambiente do IPBox.

    Args:
        navegador (webdriver.Chrome): Instância do navegador
        ambiente (str): URL do ambiente do IPBox
        login (str): Login do usuário
        senha (str): Senha do usuário
        path_log (str): Caminho para salvar os screenshots
        tipo (str): Tipo de login (ex: "ipbox", "ipbox2", "ipbox3")

    Returns:
        webdriver.Chrome: Instância do navegador após o login
    """

    if not isinstance(navegador, webdriver.Chrome):
        raise Exception("Navegador não é uma instância válida de webdriver.Chrome")
    if not isinstance(ambiente, str):
        if "http" not in ambiente:
            raise Exception("Ambiente não é uma instância válida de str")
    if (
        not isinstance(login, str)
        or not isinstance(senha, str)
        or not isinstance(path_log, str)
    ):
        raise Exception("Login, senha e path_log devem ser instâncias válidas de str")

    from selenium.webdriver.common.by import By

    screnshot_login_inicio = os.path.join(path_log, f"{tipo}_login_iniciar.png")
    screnshot_login_final = os.path.join(path_log, f"{tipo}_login_final.png")

    try:
        navegador.get(ambiente)
        navegador.save_screenshot(screnshot_login_inicio)
        navegador.find_element(By.ID, "login").send_keys(login)
        navegador.find_element(By.ID, "senha").send_keys(senha)
        navegador.find_element(By.ID, "Login").click()
        navegador.save_screenshot(screnshot_login_final)
        return navegador
    except Exception as e:
        raise Exception(f"Erro ao realizar login, detalhes: {str(e)}")


def coletar_dados_ipbox(
    navegador: webdriver.Chrome,
    dados_originais: dict,
    path_log: str,
    relatorios: list,
    tipo: str,
    lista_padrao: list,
) -> tuple:
    """
    Coleta os dados do IPBox, para relatorios definidos (filas; lotes; mailing).

    Args:
        navegador (webdriver.Chrome): Instância do navegador
        dados_originais (dict): Dicionário com modelo de dados a ser preenchido
        path_log (str): Caminho para salvar os screenshots
        relatorios (list): Lista de URLs dos relatórios a serem coletados
        tipo (str): Tipo de coleta (ex: "ipbox", "ipbox2", "ipbox3")
        lista_padrao (list): Lista de padrões para identificar as filas (padrões comuns que aparecem no nome das filas)

    Returns:
        tuple: Instância do navegador, lista de filas operando, dicionário com os dados preenchidos
    """

    if not isinstance(navegador, webdriver.Chrome):
        raise Exception("Navegador não é uma instância válida de webdriver.Chrome")
    if not isinstance(dados_originais, dict):
        raise Exception("Dados originais não são uma instância válida de dict")
    if not isinstance(path_log, str):
        raise Exception("Path_log não é uma instância válida de str")

    from selenium.webdriver.common.by import By
    from .auxiliar import acessar_pagina, extrair_tabela_ipbox

    try:

        relatorio_atual = str()
        filas_operando = list()

        for url in relatorios:

            if "listFila" in url:
                relatorio_atual = "relatorio_filas"
                salvar1 = os.path.join(path_log, f"{tipo}_filas_iniciar.png")
                salvar2 = os.path.join(path_log, f"{tipo}_filas_final.png")
            elif "listLote" in url:
                relatorio_atual = "relatorio_lotes"
                salvar1 = os.path.join(path_log, f"{tipo}_lotes_iniciar.png")
                salvar2 = os.path.join(path_log, f"{tipo}_lotes_final.png")
            elif "listMonImport" in url:
                relatorio_atual = "relatorio_mailing"
                salvar1 = os.path.join(path_log, f"{tipo}_mailing_iniciar.png")
                salvar2 = os.path.join(path_log, f"{tipo}_mailing_final.png")
            else:
                raise Exception("Relatório não identificado")

            navegador = acessar_pagina(navegador, url, salvar1, salvar2)
            res = extrair_tabela_ipbox(navegador, relatorio_atual)
            tabela = res[0]
            navegador = res[1]
            id_ilha = 0

            for linha in str(tabela).split("\n"):

                linha = linha.strip().upper()

                if linha == "":
                    continue

                if relatorio_atual == "relatorio_filas":
                    if (
                        any(fila in linha for fila in lista_padrao)
                        and "ID" not in linha
                        and "DESCRICAO" not in linha
                    ):
                        if linha not in dados_originais:
                            filas_operando.append(str(linha))
                            dados_originais[linha]
                    try:
                        canal = int(linha)
                        linha_fila = (
                            str(tabela).split("\n")[id_ilha - 4].strip().upper()
                        )
                        if linha_fila in filas_operando:
                            dados_originais[linha_fila]["canais"] = canal
                    except:
                        pass

                elif relatorio_atual == "relatorio_lotes":
                    if (
                        any(fila in linha for fila in lista_padrao)
                        and "ID" not in linha
                        and "DESCRICAO" not in linha
                    ):
                        dados = str(linha).split()
                        id_lote = int(dados[0])
                        quantidade_total = int(dados[-1].replace(".", ""))
                        quantidade_trabalhada = int(dados[-3].replace(".", ""))
                        resto = " ".join(dados[1:-4])
                        fila, descricao_lote = next(
                            (
                                (f, resto.split(f)[0].strip())
                                for f in filas_operando
                                if f in resto
                            ),
                            ("", resto),
                        )
                        dados_originais[fila]["id_lote_rodando"] = id_lote
                        dados_originais[fila]["descricao_lote_rodando"] = descricao_lote
                        dados_originais[fila]["qtd_trabalhada"] = quantidade_total
                        dados_originais[fila]["qtd_total"] = quantidade_trabalhada

                elif relatorio_atual == "relatorio_mailing":
                    id_importacao = str(linha).split()[0]

                    if id_importacao.isdigit():
                        nova_linha = (
                            str(linha)
                            + " "
                            + str(tabela).split("\n")[id_ilha + 1].strip().upper()
                        )
                        if any(fila in nova_linha for fila in lista_padrao):

                            dados = nova_linha.split()
                            data_importacao = dados[1]
                            arquivo_importacao = dados[3]
                            novos_na_fila = int(dados[-3])
                            atualizados_na_fila = int(dados[-2])
                            resto = " ".join(dados[6:-4])
                            fila = next((f for f in filas_operando if f in resto), "")
                            arquivo_importacao = arquivo_importacao.replace(
                                "-", "_"
                            ).replace(".CSV", "")
                            dados_arquivo = arquivo_importacao.split("_")
                            grupo = dados_arquivo[-2]
                            giro = dados_arquivo[-1]
                            info = "_".join(dados_arquivo[-2:])

                            dados_originais[fila]["id_ultimo_mailing"] = id_importacao
                            dados_originais[fila][
                                "arquivo_ultimo_mailing"
                            ] = arquivo_importacao
                            dados_originais[fila]["grupo_ultimo_mailing"] = grupo
                            dados_originais[fila]["giro_ultimo_mailing"] = giro
                            dados_originais[fila]["info_ultimo_mailing"] = info
                            dados_originais[fila]["novos"] = novos_na_fila
                            dados_originais[fila]["atualizados"] = atualizados_na_fila
                            dados_originais[fila][
                                "data_ultima_importacao"
                            ] = data_importacao

                else:
                    raise Exception("Relatório não identificado")

                id_ilha += 1

        return (navegador, filas_operando, dados_originais)

    except Exception as e:
        raise Exception(f"Erro ao coletar dados do IPBox, detalhes: {str(e)}")
