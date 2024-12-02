import logging


def monitorar_urazap(logging: logging.Logger) -> list:
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
        ambiente_urazap,
        login_urazap,
        senha_urazap,
        dados_urazap,
        relatorios_urazap,
        lista_padrao_filas_urazap,
        path_log,
    )
    import time, sys

    logging.info("monitorar_inove >> urazap >>Aplicacao iniciada!")
    alertas = list()

    try:
        logging.info("monitorar_inove >> urazap >>Criando navegador...")

        browser = criar_navegador(True)
        time.sleep(2)

        logging.info("monitorar_inove >> urazap >>Navegador criado com sucesso!")
    except Exception as e:
        logging.error(
            f"monitorar_inove >> urazap >>Erro ao criar o navegador, detalhes: {str(e)}"
        )
        sys.exit(1)

    try:
        logging.info("monitorar_inove >> urazap >>Realizar login no navegador...")

        browser = realizar_login_ipbox(
            browser, ambiente_urazap, login_urazap, senha_urazap, path_log, "urazap"
        )
        time.sleep(2)

        logging.info("monitorar_inove >> urazap >>Login realizado com sucesso!")
    except Exception as e:
        logging.error(
            f"monitorar_inove >> urazap >>Erro ao realizar login, detalhes: {str(e)}"
        )
        sys.exit(1)

    try:
        logging.info("monitorar_inove >> urazap >>Coletar informacoes no navegador...")

        res = coletar_dados_ipbox(
            browser,
            dados_urazap,
            path_log,
            relatorios_urazap,
            "urazap",
            lista_padrao_filas_urazap,
        )
        time.sleep(2)
        browser = res[0]
        filas = res[1]
        dados_urazap = res[2]

        logging.info("monitorar_inove >> urazap >>Informacoes coletadas com sucesso!")
    except Exception as e:
        logging.error(
            f"monitorar_inove >> urazap >>Erro ao coletar informacoes, detalhes: {str(e)}"
        )
        sys.exit(1)

    try:
        logging.info("monitorar_inove >> urazap >>Fechando navegador...")

        browser.quit()
        time.sleep(2)

        logging.info("monitorar_inove >> urazap >>Navegador fechado com sucesso!")
    except Exception as e:
        logging.error(
            f"monitorar_inove >> urazap >>Erro ao fechar o navegador, detalhes: {str(e)}"
        )
        sys.exit(1)

    try:
        logging.info("monitorar_inove >> urazap >>Apresentando informacoes...")

        logging.info(f"Filas operando: {filas}")
        for f in filas:

            logging.info(f"Fila: {f} - Dados: {dados_urazap[f]}")

            critico, tempo = verifica_tempo_operacao(
                registro_total=int(dados_urazap[f]["qtd_total"]),
                registro_consumido=int(dados_urazap[f]["qtd_trabalhada"]),
                canais=int(dados_urazap[f]["canais"]),
                operacao="IPBOX",
            )
            logging.info(f"Criticidade: {str(critico)}")
            logging.info(f"Tempo: {str(tempo)}")

            importacao = post_acompanhamento(
                "IPBOX_ZAP",
                f,
                dados_urazap[f]["info_ultimo_mailing"],
                tempo,
                critico,
                dados_urazap[f]["canais"],
                dados_urazap[f]["qtd_total"],
                dados_urazap[f]["qtd_trabalhada"],
            )
            logging.info(f"Importacao na API: {str(importacao)}")

            if critico == "nao vai durar":
                alerta = str("")
                alertas.append(alerta)

        logging.info(
            "monitorar_inove >> urazap >>Informacoes apresentadas com sucesso!"
        )
    except Exception as e:
        logging.error(
            f"monitorar_inove >> urazap >>Erro ao apresentar informacoes, detalhes: {str(e)}"
        )
        sys.exit(1)

    logging.info("monitorar_inove >> urazap >>Aplicacao finalizada!")
    return alertas
