from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from modules import post_acompanhamento, enviar_mensagem
from settings import (
    nome_log,
    path_log,
    setup_log,
    ambiente_vonix,
    login_vonix,
    senha_vonix,
    dialer_vonix,
)
import logging, time

logging.getLogger(setup_log(nome_log, path_log))


def criar_navegador(headless: bool = True) -> webdriver.Chrome:
    """
    Construir um navegador Selenium, deixando-o usual.
    """
    try:
        opcoes = Options()
        if headless:
            opcoes.add_argument("--headless")
        browser = webdriver.Chrome(options=opcoes)
        browser.implicitly_wait(2)
        return browser
    except Exception as e:
        raise Exception(f"Impossível criar o navegador, detalhes: {str(e)}")


def realizar_login(
    navegador: webdriver.Chrome, ambiente: str, login: str, senha: str
) -> webdriver.Chrome:
    """
    Realiza o login

    Entrada:
        navegador(webdriver.Chrome): recebe um navegador ativo que seja comandado pelo mesmo.
        ambiente (str): url para fazer login
        login (str): login
        senha (str): senha

    Saída:
        O navegador com instância ativa do Nossa URA
    """

    from selenium.webdriver.common.by import By
    from settings import path_log
    import os
    import time

    realizar_login = os.path.join(path_log, "login.png")
    realizar_login_feito = os.path.join(path_log, "login_feito.png")

    try:
        navegador.get(ambiente)
        time.sleep(10)
        navegador.save_screenshot(realizar_login)

        username = navegador.find_element(By.ID, "username")
        password = navegador.find_element(By.ID, "password")

        if username.is_displayed() and password.is_displayed():
            username.send_keys(str(login))
            password.send_keys(str(senha))

        login_button = navegador.find_element(By.NAME, "commit")
        if login_button.is_displayed():
            login_button.click()
        navegador.save_screenshot(realizar_login_feito)

        return navegador
    except Exception as e:
        raise Exception(f"Impossivel logar em Vonix_Nuvonix, detalhes: {str(e)}")


def puxar_informacoes(navegador: webdriver.Chrome, dialer: str):

    from settings import path_log
    import os, time
    from selenium.webdriver.common.by import By

    pagina_infos = os.path.join(path_log, "dialer.png")

    try:
        navegador.get(dialer)
        time.sleep(10)
        navegador.save_screenshot(pagina_infos)
        dados = []

        table = navegador.find_element(By.ID, "active_table").text
        table = str(table).split("\n")
        for linhas in table:
            if "Pausar" not in linhas:
                if "Fila" not in linhas:
                    linha = str(linhas).split(" ")
                    fila = linha[0] + "_" + linha[1] + "_" + linha[2] + "_" + linha[4]
                    status = linha[5]
                    fila = str(fila).upper()
                    contatos = linha[-4]
                    canais = linha[-3]
                    if status == "Discando":
                        dados.append((fila, contatos, canais))

        return (navegador, dados)
    except Exception as e:
        raise Exception(
            f"Impossivel navegar ate dialer Vonix_Nuvonix, detalhes: {str(e)}"
        )


def verifica_tempo_operacao(
    registro_total: int, canais: int, operacao: str = ""
) -> str:
    """
    Realiza o calculo de tempo de operacao e informa se a operacao vai ou nao durar nos proximos 30 minutos ( tempo = registros / 70 * canais ) .

    Entrada:
        registro_total (int): inteiro representando o número de registros total
        registro_consumido (int): inteiro representando o número de registros consumidos
        canais (int): inteiro representando quantidade de canais
        opercao (str): representando qual ambiente de analise é

    Saída:
        string representando 'vai durar' caso o valor de T for maior que 0.5 ou 'nao vai durar' caso seja menor ou igual a 0.5
    """

    if operacao not in ["NOSSA URA", "IPBOX", "IPBOX2", "VONIX"]:
        raise Exception("Opa... Operacao invalida")
    elif operacao == "NOSSA URA":
        valor_operacao = 54
    elif operacao == "IPBOX":
        valor_operacao = 75
    elif operacao == "IPBOX2":
        valor_operacao = 75
    elif operacao == "VONIX":
        valor_operacao = 80

    if canais == 0:
        canais = 1

    try:
        registros = registro_total
        criticidade = "vai durar"
    except:
        raise Exception(
            "Opa... Os registros foram passados errados, registro_total precisa ser maior do que registro_consumido"
        )

    try:
        registros = int(registros)
        valor_operacao = int(valor_operacao)
        canais = int(canais)
        tempo_operacao = registros / (valor_operacao * canais)
        print(tempo_operacao)
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
    except:
        raise Exception("Opa... Nao foi possivel fazer os calculos")

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


def monitorar_vonix():

    try:
        alertas = []
        logging.info("bot_vonix_monitoria >> inicio")

        navegador = criar_navegador(True)
        logging.info("bot_vonix_monitoria >> Navegador construido!")
        time.sleep(2)

        navegador = realizar_login(navegador, ambiente_vonix, login_vonix, senha_vonix)
        logging.info("bot_vonix_monitoria >> Sucesso ao realizar login")
        time.sleep(2)

        res = puxar_informacoes(navegador, dialer_vonix)
        navegador = res[0]
        dados_list = res[1]
        logging.info("bot_vonix_monitoria >> Sucesso ao puxar informações")
        time.sleep(2)

        for i in dados_list:
            fila = i[0]
            contatos = i[1]
            canais = i[2]
            operacao, tempo = verifica_tempo_operacao(contatos, canais, "VONIX")
            post_acompanhamento(
                "VONIX_NUVONIX", fila, "A_G1", tempo, operacao, canais, 0, contatos
            )

            if operacao == "nao vai durar":
                alertas.append(
                    str(
                        f"ATENÇÃO: Hora de alimentar Mailing <{fila}> em <VONIX_NUVONIX>"
                    )
                )

        logging.info("bot_vonix_monitoria >> final")
        return alertas
    except Exception as e:
        logging.error(f"bot_vonix_monitoria >> erro: {str(e)}")
