import datetime
from collections import defaultdict
from settings import path_data, path_doc, path_json, path_temp, path_src, path_log
import os
from dotenv import load_dotenv

load_dotenv()

filas_monitorar: dict = {
    "Expert Vendas": "00025",
    "Qualify Vendas": "00024",
    "Trainee Vendas": "00021",
}


def inicializar_dict_ipbox():
    """
    Inicializa um dicionário com as chaves necessárias para armazenar informações do IPBOX.

    Returns:
        dict: Dicionário inicializado com as chaves necessárias.
    """

    return {
        "canais": 0,
        "id_lote_rodando": 0,
        "descricao_lote_rodando": "",
        "qtd_trabalhada": 0,
        "qtd_total": 0,
        "id_ultimo_mailing": 0,
        "arquivo_ultimo_mailing": "",
        "grupo_ultimo_mailing": "",
        "giro_ultimo_mailing": "",
        "info_ultimo_mailing": "A_G1",
        "novos": 0,
        "atualizados": 0,
        "data_ultima_importacao": "",
    }


# Pastas que serão criadas caso não existam
lista_pastas = []
lista_pastas.append(path_data)
lista_pastas.append(path_doc)
lista_pastas.append(path_json)
lista_pastas.append(path_temp)
lista_pastas.append(path_src)
lista_pastas.append(path_log)

# Pacotes que serão instalados caso não existam
lista_pacotes = []
lista_pacotes.append("python-dotenv")
lista_pacotes.append("pandas")
lista_pacotes.append("datetime")
lista_pacotes.append("selenium")
lista_pacotes.append("webdriver_manager")

# Padrão de log
nome_log = "monitorar_inove"

# Variáveis de ambiente VONIX
ambiente_vonix = os.getenv("AMBIENTE_VONIX")
dialer_vonix = os.getenv("DIALER_VONIX")
login_vonix = os.getenv("LOGIN_VONIX")
senha_vonix = os.getenv("SENHA_VONIX")

# Variáveis de ambiente URAVOZ
ambiente_uravoz = os.getenv("AMBIENTE_URAVOZ")
login_uravoz = os.getenv("LOGIN_URAVOZ")
senha_uravoz = os.getenv("SENHA_URAVOZ")
filasativas_uravoz = ambiente_uravoz + "/listFila.php?tipo=A&selectActive=Y"
lotesrodando_uravoz = ambiente_uravoz + "/listLote.php?selectStatus=R"
mailingrodando_uravoz = ambiente_uravoz + "/listMonImport.php"
relatorios_uravoz = []
relatorios_uravoz.append(filasativas_uravoz)
relatorios_uravoz.append(lotesrodando_uravoz)
relatorios_uravoz.append(mailingrodando_uravoz)
dados_uravoz = defaultdict(inicializar_dict_ipbox)
lista_padrao_filas_uravoz = [
    "NIVA",
    "RCS",
    "RSN",
    "RCO",
    "RNN",
    "RSU",
    "RSE",
    "OF FILIAL",
]

# Variáveis de ambiente URAVOZ2
ambiente_uravoz2 = os.getenv("AMBIENTE_URAVOZ2")
login_uravoz2 = os.getenv("LOGIN_URAVOZ2")
senha_uravoz2 = os.getenv("SENHA_URAVOZ2")
filasativas_uravoz2 = ambiente_uravoz2 + "/listFila.php?tipo=A&selectActive=Y"
lotesrodando_uravoz2 = ambiente_uravoz2 + "/listLote.php?selectStatus=R"
mailingrodando_uravoz2 = ambiente_uravoz2 + "/listMonImport.php"
relatorios_uravoz2 = []
relatorios_uravoz2.append(filasativas_uravoz2)
relatorios_uravoz2.append(lotesrodando_uravoz2)
relatorios_uravoz2.append(mailingrodando_uravoz2)
dados_uravoz2 = defaultdict(inicializar_dict_ipbox)
lista_padrao_filas_uravoz2 = ["URA MEI"]

# Variáveis de ambiente URAZAP
ambiente_urazap = os.getenv("AMBIENTE_URAZAP")
login_urazap = os.getenv("LOGIN_URAZAP")
senha_urazap = os.getenv("SENHA_URAZAP")
filasativas_urazap = ambiente_urazap + "/listFila.php?tipo=A&selectActive=Y"
lotesrodando_urazap = (
    ambiente_urazap + "/listLote.php?selectStatus=R&order=lote.id%20ASC"
)
mailingrodando_urazap = ambiente_urazap + "/listMonImport.php"
relatorios_urazap = []
relatorios_urazap.append(filasativas_urazap)
relatorios_urazap.append(lotesrodando_urazap)
relatorios_urazap.append(mailingrodando_urazap)
dados_urazap = defaultdict(inicializar_dict_ipbox)
lista_padrao_filas_urazap = ["FILA ", "OFERTA "]

# Variaveis para controle de periodo de execução
periodos_execucao: dict = {
    "monday": {"inicio": datetime.time(8, 0), "fim": datetime.time(19, 0)},
    "tuesday": {"inicio": datetime.time(8, 0), "fim": datetime.time(19, 0)},
    "wednesday": {"inicio": datetime.time(8, 0), "fim": datetime.time(19, 0)},
    "thursday": {"inicio": datetime.time(8, 0), "fim": datetime.time(19, 0)},
    "friday": {"inicio": datetime.time(8, 0), "fim": datetime.time(19, 0)},
    # "saturday": {"inicio": datetime.time(8, 0), "fim": datetime.time(13, 0)}
}

# Variaveis monitorias
ambiente_monitorialeads = ambiente_uravoz
ambiente_nossaura: str = os.getenv("AMBIENTE_URAZAP")
campanha_nossaura: str = os.getenv("CAMPANHA_NOSSAURA")
login_nossaura: str = os.getenv("LOGIN_NOSSAURA")
senha_nossaura: str = os.getenv("SENHA_NOSSAURA")
