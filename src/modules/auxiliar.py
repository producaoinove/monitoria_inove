from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def criar_navegador(ocultar_navegador: bool = True) -> webdriver.Chrome:
    """
    Cria um navegador acessivel por selenium.

    Args:
        ocultar_navegador (bool, optional): Se True, o navegador será ocultado. Default - True.

    Returns:
        webdriver.Chrome: Navegador acessível por selenium.
    """
    try:
        opcoes = Options()
        if ocultar_navegador:
            opcoes.add_argument("--headless=new")
        opcoes.add_argument("--no-sandbox")
        opcoes.add_argument("--disable-dev-shm-usage")
        opcoes.add_argument("--disable-gpu")
        browser = webdriver.Chrome(options=opcoes)
        return browser
    except Exception as e:
        raise Exception(f"Impossível criar o navegador, detalhes: {str(e)}")


def acessar_pagina(
    navegador: webdriver.Chrome, url: str, png1: str, png2: str
) -> webdriver.Chrome:
    """
    Tenta acessar a página desejada e salva dois prints da tela (antes e depois).

    Args:
        navegador (webdriver.Chrome): Navegador acessível por selenium.
        url (str): URL da página a ser acessada.
        png1 (str): Nome do arquivo de imagem a ser salvo antes do acesso.
        png2 (str): Nome do arquivo de imagem a ser salvo depois do acesso.

    Returns:
        webdriver.Chrome: Navegador acessível por selenium.
    """
    try:
        if not isinstance(navegador, webdriver.Chrome):
            raise Exception("Navegador não é uma instância válida de webdriver.Chrome")
        if not isinstance(url, str):
            raise Exception("URL não é uma instância válida de str")
        if not isinstance(png1, str) or not isinstance(png2, str):
            if ".png" not in png1 or ".png" not in png2:
                raise Exception("PNG1 e PNG2 devem ser instâncias válidas de str")
        navegador.save_screenshot(png1)
        navegador.get(url)
        navegador.save_screenshot(png2)
        return navegador
    except Exception as e:
        raise Exception(f"Erro ao acessar a página, detalhes: {str(e)}")


def extrair_tabela_ipbox(navegador: webdriver.Chrome, relatorio: str) -> tuple:
    """
    Extrai a tabela de um relatório do IPBOX.

    Args:
        navegador (webdriver.Chrome): Navegador acessível por selenium.
        relatorio (str): Nome do relatório a ser extraído.

    Returns:
        tuple: Tupla contendo a tabela extraída e o navegador.
    """
    try:
        if not isinstance(navegador, webdriver.Chrome):
            raise Exception("Navegador não é uma instância válida de webdriver.Chrome")
        if not isinstance(relatorio, str):
            raise Exception("Relatório não é uma instância válida de str")
        from selenium.webdriver.common.by import By

        tabela = navegador.find_element(by=By.CLASS_NAME, value="grid").text
        return (tabela, navegador)
    except Exception as e:
        raise Exception(f"Erro ao extrair a tabela, detalhes: {str(e)}")
