import time
def executar_monitorleads() -> list:
    """
    Realiza a execução do bot de monitoramento de leads.

    Entrada:
        Nenhuma

    Saída:
        list: mensagens de alerta para cada fila
    """

    from settings import (
        path_log,
        path_data,
        filas_monitorar,
        setup_log,
        ambiente_monitorialeads,
    )
    from .functions import (
        pegar_id_fila_monitorialeads,
        pegar_timestamp,
        construir_url_monitorialeads,
        extrair_dados_monitorialeads,
        extracao_monitorialeads,
    )
    import logging
    from datetime import datetime
    import os

    logging.getLogger(setup_log("monitorar_leads", path_log))
    logging.info("Iniciando aplicacao")
    resultado = list()
    cancelar = False

    try:
        logging.info("Executando rotina de monitoramento de leads")

        try:
            timestamps = pegar_timestamp()
            inicio = timestamps[0]
            final = timestamps[1]
            logging.info(f"Timestamps construidos: de {inicio} ate {final}")
        except Exception as e:
            logging.error(f"Erro ao coletar timestamps: {e}")
            raise e

        try:

            for nome_fila in filas_monitorar:

                try:
                    id_fila = pegar_id_fila_monitorialeads(nome_fila)
                    logging.info(f"ID da fila {nome_fila}: {id_fila}")
                except Exception as e:
                    logging.error(f"Erro ao coletar ID da fila {nome_fila}: {e}")

                try:
                    url_anlise = construir_url_monitorialeads(
                        ambiente_monitorialeads, id_fila, inicio, final
                    )
                    logging.info(f"URL da fila {nome_fila}: {url_anlise}")
                except Exception as e:
                    logging.error(f"Erro ao construir URL da fila {nome_fila}: {e}")

                try:
                    dados = extrair_dados_monitorialeads(url_anlise)

                    carimbo = dados[0]
                    telefone = dados[1]
                    logging.info(f"Dados extraidos da fila {nome_fila}: {dados}")
                except Exception as e:
                    if "nao" in str(e):
                        logging.info(f"Nao ha chamadas na fila {nome_fila}")
                        cancelar = True
                    else:
                        logging.error(f"Erro ao extrair dados da fila {nome_fila}: {e}")
                        cancelar = True

                if cancelar == False:

                    hoje = datetime.now().strftime("%Y.%m.%d")
                    fila = str(nome_fila).replace(" ", "").lower()
                    file_save = f"{fila}_{hoje}.csv"
                    path_file = os.path.join(path_data, file_save)

                    try:
                        verificado = extracao_monitorialeads(
                            path_file, carimbo, telefone
                        )
                        logging.info(
                            f"Extracao da fila {nome_fila} salva em {path_file}"
                        )
                    except Exception as e:
                        logging.error(
                            f"Erro ao salvar extracao da fila {nome_fila}: {e}"
                        )

                    if verificado == True:
                        logging.info(
                            f"Extracao da fila {nome_fila} verificada com sucesso"
                        )
                        logging.info("Nenhuma acao realizada!")
                    else:
                        logging.info(f"Extracao da fila {nome_fila} nao verificada")
                        logging.info("Avisar nos canais de comunicacao")
                        resultado.append(
                            str(
                                f"ATENÇÃO: Fila {nome_fila} está sem leads há mais de 5min"
                            )
                        )

            return resultado

        except Exception as e:
            logging.error(f"Erro ao coletar IDs de filas: {e}")
            raise e

    except Exception as e:
        logging.error(f"Erro ao executar rotina de monitoramento de mailing: {e}")
    finally:
        logging.info("Finalizando aplicacao")
