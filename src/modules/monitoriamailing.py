import logging
import time


def monitorar_mailing() -> list:
    """
    Raiz do monitoria de mailing para controlar execucao do bot

    Entrada:
        nenhuma

    Saída:
        uma lista com os alertas a serem enviados.
    """

    from .functions import (
        verifica_tempo_operacao,
        realizar_login,
        ir_campanha,
        extracao_campanha_nossaura,
        tratar_dados_campanha,
        post_acompanhamento,
    )
    from .auxiliar import criar_navegador
    from settings import (
        ambiente_nossaura,
        login_nossaura,
        senha_nossaura,
        campanha_nossaura,
        path_log,
        setup_log,
    )

    logging.getLogger(setup_log("monitorar", path_log))
    resultado = list()

    try:

        browser = criar_navegador(True)
        logging.info("Navegador criado!")

    except Exception as e:
        logging.error(f"Impossivel criar navegador, detalhes: {str(e)}")
        raise e

    try:

        browser = realizar_login(
            browser, ambiente_nossaura, login_nossaura, senha_nossaura
        )
        logging.info("Login realizado!")

    except Exception as e:
        logging.error(f"Impossivel realizar login, detalhes: {str(e)}")
        return "Falha no login"

    try:

        browser = ir_campanha(browser, campanha_nossaura)
        logging.info("Ida ate a pagina da campanha!")

    except Exception as e:
        logging.error(f"Impossivel ir ate a campanha, detalhes: {str(e)}")
        raise e

    try:

        dados_extraidos = extracao_campanha_nossaura(browser)
        logging.info("Dados extraidos!")

    except Exception as e:
        logging.error(f"Impossivel extrair os dados da campanha, detalhes: {str(e)}")
        raise e

    try:
        dados = tratar_dados_campanha(dados_extraidos)
        logging.info("Dados da campanha, tratados!")

    except Exception as e:
        logging.error(f"Impossivel tratar os dados da campanha, detalhes: {str(e)}")
        raise e

    for item in dados:

        fila = item[0]
        reg_c = item[1]
        reg_t = item[2]
        canais = item[3]

        try:
            nome_fila = str(fila).replace("-", "_").split("_")
            fila_save = nome_fila[0] + "_" + nome_fila[1]
        except:
            fila_save = nome_fila
        giro = nome_fila[2]
        ultimo_mailing = giro + "_G1"

        logging.info(
            f"Na fila {str(fila)} tem {str(reg_t)} registros totais e {str(canais)} canais. Dos quais {str(reg_c)} registros foram consumidos."
        )

        res = verifica_tempo_operacao(reg_t, reg_c, canais, "NOSSA URA")
        operacao = res[0]
        tempo = res[1]

        post_acompanhamento(
            "NOSSA_URA",
            fila_save,
            ultimo_mailing,
            tempo,
            operacao,
            canais,
            reg_t,
            reg_c,
        )

        logging.info(operacao)
        if "nao" in operacao:
            resultado.append(
                str(f"ATENÇÃO: Hora de alimentar Mailing <{fila}> em <Nossa URA>")
            )

    return resultado
