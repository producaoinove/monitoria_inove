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
        monitorar_uravoz,
        monitorar_uravoz2,
        monitorar_urazap,
        criar_navegador,
        logar_no_whatsapp,
        enviar_mensagem,
        monitorar_vonix,
        executar_monitorleads,
        monitorar_mailing,
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

        agora = datetime.datetime.now().time()
        dia_semana = datetime.datetime.now().strftime("%A").lower()

        if (
            dia_semana in periodos_execucao
            and periodos_execucao[dia_semana]["inicio"]
            <= agora
            <= periodos_execucao[dia_semana]["fim"]
        ):

            try:
                logging.info("monitorar_inove >> Inicio monitoramento dos leads...")

                lista_alertas = executar_monitorleads()
                if lista_alertas != None:

                    logging.info(
                        f"Total de alertas gerados em MONITORIA LEADS: {str(lista_alertas.__len__())}"
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
                                )
                                logging.info("Alerta enviado")
                                time.sleep(10)
                            except Exception as e:
                                logging.error(f"Impossivel enviar alerta: {str(e)}")

                logging.info("monitorar_inove >> Fim monitoramento leads!")
            except Exception as e:
                logging.error(
                    f"monitorar_inove >> Erro ao monitorar leads, detalhes: {str(e)}"
                )
                sys.exit(1)

            try:
                logging.info("monitorar_inove >> Inicio monitoramento uravoz...")

                lista_alertas = monitorar_uravoz(logging)
                if lista_alertas != None:

                    logging.info(
                        f"Total de alertas gerados em MONITORIA MAILING IPBOX_VOZ: {str(lista_alertas.__len__())}"
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
                                )
                                logging.info("Alerta enviado")
                                time.sleep(10)
                            except Exception as e:
                                logging.error(f"Impossivel enviar alerta: {str(e)}")

                logging.info("monitorar_inove >> Fim monitoramento uravoz!")
            except Exception as e:
                logging.error(
                    f"monitorar_inove >> Erro ao monitorar uravoz, detalhes: {str(e)}"
                )
                sys.exit(1)

            try:
                logging.info("monitorar_inove >> Inicio monitoramento uravoz2...")

                lista_alertas = monitorar_uravoz2(logging)
                if lista_alertas != None:

                    logging.info(
                        f"Total de alertas gerados em MONITORIA MAILING IPBOX_VOZ2: {str(lista_alertas.__len__())}"
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
                                )
                                logging.info("Alerta enviado")
                                time.sleep(10)
                            except Exception as e:
                                logging.error(f"Impossivel enviar alerta: {str(e)}")

                logging.info("monitorar_inove >> Fim monitoramento uravoz2!")
            except Exception as e:
                logging.error(
                    f"monitorar_inove >> Erro ao monitorar uravoz2, detalhes: {str(e)}"
                )
                sys.exit(1)

            try:
                logging.info("monitorar_inove >> Inicio monitoramento urazap...")

                lista_alertas = monitorar_urazap(logging)
                if lista_alertas != None:

                    logging.info(
                        f"Total de alertas gerados em MONITORIA MAILING IPBOX_ZAP: {str(lista_alertas.__len__())}"
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
                                )
                                logging.info("Alerta enviado")
                                time.sleep(10)
                            except Exception as e:
                                logging.error(f"Impossivel enviar alerta: {str(e)}")

                logging.info("monitorar_inove >> Fim monitoramento urazap!")
            except Exception as e:
                logging.error(
                    f"monitorar_inove >> Erro ao monitorar urazap, detalhes: {str(e)}"
                )
                sys.exit(1)

            try:
                logging.info("monitorar_inove >> Inicio monitoramento dos NOSSA_URA...")

                lista_alertas = monitorar_mailing()
                if lista_alertas != None:

                    logging.info(
                        f"Total de alertas gerados em MONITORIA NOSSA_URA: {str(lista_alertas.__len__())}"
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
                                    logging,
                                )
                                logging.info("Alerta enviado")
                                time.sleep(10)
                            except Exception as e:
                                logging.error(f"Impossivel enviar alerta: {str(e)}")

                logging.info("monitorar_inove >> Fim monitoramento NOSSA_URA!")
            except Exception as e:
                logging.error(
                    f"monitorar_inove >> Erro ao monitorar NOSSA_URA, detalhes: {str(e)}"
                )
                sys.exit(1)

            try:
                logging.info("monitorar_inove >> Inicio monitoramento dos VONIX...")

                lista_alertas = monitorar_vonix()
                if lista_alertas != None:

                    logging.info(
                        f"Total de alertas gerados em MONITORIA VONIX: {str(lista_alertas.__len__())}"
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
                                )
                                logging.info("Alerta enviado")
                                time.sleep(10)
                            except Exception as e:
                                logging.error(f"Impossivel enviar alerta: {str(e)}")

                logging.info("monitorar_inove >> Fim monitoramento VONIX!")
            except Exception as e:
                logging.error(
                    f"monitorar_inove >> Erro ao monitorar VONIX, detalhes: {str(e)}"
                )
                sys.exit(1)

        else:
            logging.info("Fora do horário de execução")

        import time

        time.sleep(300)

        logging.info("monitorar_inove >> Aplicacao finalizada!")
