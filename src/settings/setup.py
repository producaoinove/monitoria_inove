import logging
import os
import subprocess
import sys

def instalar_pacotes_externos(pacote: str) -> None:
    """
Instala o pacote especificado usando pip.

Entrada:
    pacote (str): o nome do pacote a ser instalado

Saída:
    nenhuma (none)
    """
    try:
        os.system("python.exe -m pip install --upgrade pip")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pacote])
    except subprocess.CalledProcessError as e:
        print(f"Erro ao instalar o pacote {pacote}: {e}")
        raise

def setup_log(nome_log: str, path_log: str) -> logging.Logger:
    log_file = os.path.join(path_log, nome_log + ".log")
    logger = logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    return logger


def validar_pastas(lista_pastas: list) -> bool:
    """
Verifica as pastas necessárias ao projeto e cria se necessário.

Entrada:
    pastas (list): uma lista com caminhos (absolutos) das pastas necessárias ao projeto

Saída:
    uma string avisando que verificou e criou se necessário
    """
    for pasta in lista_pastas:
        if not os.path.exists(pasta):
            os.makedirs(pasta)
    
    return "Pastas verificadas e criadas, se necessário."


def validar_pacotes(lista_pacotes: list) -> bool:
    """
Verifica se os pacotes estão instalados, caso contrário, instala-os.

Entrada:
    pacotes (list): uma lista de strings com os nomes dos pacotes a serem verificados

Saída:
    nenhuma (none)
    """
    for pacote in lista_pacotes:
        try:
            __import__(pacote)
        except ImportError:
            print(f"Pacote {pacote} não encontrado. Instalando...")
            instalar_pacotes_externos(pacote)
