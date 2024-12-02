import logging


def monitorar_uravoz(logging: logging.Logger) -> list:
    """
    Função responsável por monitorar o ambiente uravoz.

    Args:
        logging (logging.Logger): Objeto de logging ( com configurações básicas ).

    Returns:
        lista com alertas de fila acabando
    """

    from modules import (
        criar_navegador,
        realizar_login_ipbox,
        coletar_dados_ipbox,
        verifica_tempo_operacao,
        post_acompanhamento,
    )
    from settings import (
        ambiente_uravoz,
        login_uravoz,
        senha_uravoz,
        dados_uravoz,
        relatorios_uravoz,
        lista_padrao_filas_uravoz,
        path_log,
    )
    import time, sys

    logging.info("monitorar_inove >> uravoz >>Aplicacao iniciada!")
    alertas = list()

    try:
        logging.info("monitorar_inove >> uravoz >>Criando navegador...")

        browser = criar_navegador(True)
        time.sleep(2)

        logging.info("monitorar_inove >> uravoz >>Navegador criado com sucesso!")
    except Exception as e:
        logging.error(
            f"monitorar_inove >> uravoz >>Erro ao criar o navegador, detalhes: {str(e)}"
        )
        sys.exit(1)

    try:
        logging.info("monitorar_inove >> uravoz >>Realizar login no navegador...")

        browser = realizar_login_ipbox(
            browser, ambiente_uravoz, login_uravoz, senha_uravoz, path_log, "uravoz"
        )
        time.sleep(2)

        logging.info("monitorar_inove >> uravoz >>Login realizado com sucesso!")
    except Exception as e:
        logging.error(
            f"monitorar_inove >> uravoz >>Erro ao realizar login, detalhes: {str(e)}"
        )
        sys.exit(1)

    try:
        logging.info("monitorar_inove >> uravoz >>Coletar informacoes no navegador...")

        res = coletar_dados_ipbox(
            browser,
            dados_uravoz,
            path_log,
            relatorios_uravoz,
            "uravoz",
            lista_padrao_filas_uravoz,
        )
        time.sleep(2)
        browser = res[0]
        filas = res[1]
        dados_uravoz = res[2]

        logging.info("monitorar_inove >> uravoz >>Informacoes coletadas com sucesso!")
    except Exception as e:
        logging.error(
            f"monitorar_inove >> uravoz >>Erro ao coletar informacoes, detalhes: {str(e)}"
        )
        sys.exit(1)

    try:
        logging.info("monitorar_inove >> uravoz >>Fechando navegador...")

        browser.quit()
        time.sleep(2)

        logging.info("monitorar_inove >> uravoz >>Navegador fechado com sucesso!")
    except Exception as e:
        logging.error(
            f"monitorar_inove >> uravoz >>Erro ao fechar o navegador, detalhes: {str(e)}"
        )
        sys.exit(1)

    try:
        logging.info("monitorar_inove >> uravoz >>Estudando informacoes...")

        logging.info(f"Filas operando: {filas}")
        for f in filas:

            logging.info(f"Fila: {f} - Dados: {dados_uravoz[f]}")

            critico, tempo = verifica_tempo_operacao(
                registro_total=int(dados_uravoz[f]["qtd_total"]),
                registro_consumido=int(dados_uravoz[f]["qtd_trabalhada"]),
                canais=int(dados_uravoz[f]["canais"]),
                operacao="IPBOX",
            )
            logging.info(f"Criticidade: {str(critico)}")
            logging.info(f"Tempo: {str(tempo)}")

            importacao = post_acompanhamento(
                "IPBOX_VOZ",
                f,
                dados_uravoz[f]["info_ultimo_mailing"],
                tempo,
                critico,
                dados_uravoz[f]["canais"],
                dados_uravoz[f]["qtd_total"],
                dados_uravoz[f]["qtd_trabalhada"],
            )
            logging.info(f"Importacao na API: {str(importacao)}")

            if critico == "nao vai durar":
                alerta = str("")
                alertas.append(alerta)

        logging.info("monitorar_inove >> uravoz >>Informacoes estudadas com sucesso!")
    except Exception as e:
        logging.error(
            f"monitorar_inove >> uravoz >>Erro ao estudar informacoes, detalhes: {str(e)}"
        )
        sys.exit(1)

    logging.info("monitorar_inove >> uravoz >>Aplicacao finalizada!")
    return alertas
