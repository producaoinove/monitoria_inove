import time
import logging
from collections import defaultdict

def monitorar_uravoz2(logging: logging.Logger) -> list:
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
        ambiente_uravoz2,
        login_uravoz2,
        senha_uravoz2,
        inicializar_dict_ipbox,
        relatorios_uravoz2,
        lista_padrao_filas_uravoz2,
        path_log,
    )
    import time, sys

    logging.info("monitorar_inove >> uravoz2 >>Aplicacao iniciada!")

    alertas = list()

    try:
        logging.info("monitorar_inove >> uravoz2 >>Criando navegador...")

        browser = criar_navegador(True)
        time.sleep(2)

        logging.info("monitorar_inove >> uravoz2 >>Navegador criado com sucesso!")
    except Exception as e:
        logging.error(
            f"monitorar_inove >> uravoz2 >>Erro ao criar o navegador, detalhes: {str(e)}"
        )
        sys.exit(1)

    try:
        logging.info("monitorar_inove >> uravoz2 >>Realizar login no navegador...")

        browser = realizar_login_ipbox(
            browser, ambiente_uravoz2, login_uravoz2, senha_uravoz2, path_log, "uravoz2"
        )
        time.sleep(2)

        logging.info("monitorar_inove >> uravoz2 >>Login realizado com sucesso!")
    except Exception as e:
        logging.error(
            f"monitorar_inove >> uravoz2 >>Erro ao realizar login, detalhes: {str(e)}"
        )
        sys.exit(1)

    try:
        logging.info("monitorar_inove >> uravoz2 >>Coletar informacoes no navegador...")

        dados_uravoz2 = defaultdict(inicializar_dict_ipbox)

        res = coletar_dados_ipbox(
            browser,
            dados_uravoz2,
            path_log,
            relatorios_uravoz2,
            "uravoz2",
            lista_padrao_filas_uravoz2,
        )
        time.sleep(2)
        browser = res[0]
        filas = res[1]
        dados_uravoz2 = res[2]

        logging.info("monitorar_inove >> uravoz2 >>Informacoes coletadas com sucesso!")
    except Exception as e:
        if 'list index out of range' in str(e): dados_uravoz2 = dados_uravoz2
        else:
            logging.error(
                f"monitorar_inove >> uravoz2 >>Erro ao coletar informacoes, detalhes: {str(e)}"
            )
            sys.exit(1)

    try:
        logging.info("monitorar_inove >> uravoz2 >>Fechando navegador...")

        browser.quit()
        time.sleep(2)

        logging.info("monitorar_inove >> uravoz2 >>Navegador fechado com sucesso!")
    except Exception as e:
        logging.error(
            f"monitorar_inove >> uravoz2 >>Erro ao fechar o navegador, detalhes: {str(e)}"
        )
        sys.exit(1)

    try:
        logging.info("monitorar_inove >> uravoz2 >>Apresentando informacoes...")

        logging.info(f"Filas operando: {filas}")

        for f in filas:

            logging.info(f"Fila: {f} - Dados: {dados_uravoz2[f]}")

            critico, tempo = verifica_tempo_operacao(
                registro_total=int(dados_uravoz2[f]["qtd_total"]),
                registro_consumido=int(dados_uravoz2[f]["qtd_trabalhada"]),
                canais=int(dados_uravoz2[f]["canais"]),
                operacao="IPBOX",
            )
            logging.info(f"Criticidade: {str(critico)}")
            logging.info(f"Tempo: {str(tempo)}")

            importacao = post_acompanhamento(
                "IPBOX_VOZ2",
                f,
                dados_uravoz2[f]["info_ultimo_mailing"],
                tempo,
                critico,
                dados_uravoz2[f]["canais"],
                dados_uravoz2[f]["qtd_total"],
                dados_uravoz2[f]["qtd_trabalhada"],
            )
            logging.info(f"Importacao na API: {str(importacao)}")
            if critico == "nao vai durar":
                alerta = str("")
                alertas.append(alerta)

        logging.info(
            "monitorar_inove >> uravoz2 >>Informacoes apresentadas com sucesso!"
        )
    except Exception as e:
        logging.error(
            f"monitorar_inove >> uravoz2 >>Erro ao apresentar informacoes, detalhes: {str(e)}"
        )
        sys.exit(1)

    logging.info("monitorar_inove >> uravoz2 >> Aplicacao finalizada!")
    return alertas
