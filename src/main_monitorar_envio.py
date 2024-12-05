import sys

try:

    from settings import (
        validar_pacotes,
        lista_pastas,
        validar_pastas,
        lista_pacotes,
        periodos_execucao,
    )

    print("Validando pastas e pacotes...")

    print("Lista de pacotes:", lista_pacotes)
    validar_pacotes(lista_pacotes)
    print("Lista de pastas:", lista_pastas)
    validar_pastas(lista_pastas)
    print("Pastas e pacotes validadas!")

    from settings import setup_log, path_log, nome_log
    import logging, datetime

    logging.getLogger(setup_log(nome_log, path_log)).info(
        "Log configurado com sucesso!"
    )
except Exception as e:
    print(f"Erro: {e}")
    sys.exit(1)

if __name__ == "__main__":

    from modules import (
        criar_navegador,
        logar_no_whatsapp,
        enviar_mensagem,
        monitorar_internamente
    )

    logging.info("monitorar_inove >> Aplicacao iniciada!")

    try:
        logging.info("monitorar_inove >> inicio criar browser para ZAP")

        zap_browser = criar_navegador(False)
        zap_browser = logar_no_whatsapp(zap_browser, logging)

        logging.info("monitorar_inove >> final criar browser para ZAP")
    except Exception as e:
        logging.error(f"monitorar_inove >> erro ao criar browser do ZAP {str(e)}")

    while True:

        try:
            logging.info("monitorar_inove >> Inicio monitoramento dos alertas internos...")

            lista_alertas = monitorar_internamente(logging)
            if lista_alertas != None:

                logging.info(
                    f"Total de alertas gerados em MONITORIA alertas internos: {str(lista_alertas.__len__())}"
                )

                if lista_alertas.__len__() > 0:
                    logging.info("Alertas gerados:")
                    for alerta in lista_alertas:

                        try:
                            enviar_mensagem(
                                zap_browser,
                                "grupo",
                                "CJwyombFJpVLmhNNaOJfNE",
                                alerta,
                                logging
                            )
                            logging.info("Alerta enviado")
                            time.sleep(10)
                        except Exception as e:
                            logging.error(f"Impossivel enviar alerta: {str(e)}")

            logging.info("monitorar_inove >> Fim monitoramento alertas internos!")
        except Exception as e:
            logging.error(
                f"monitorar_inove >> Erro ao monitorar alertas internos, detalhes: {str(e)}"
            )
            sys.exit(1)

        import time

        time.sleep(30)

        logging.info("monitorar_inove >> Aplicacao finalizada!")
