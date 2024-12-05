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
        monitorar_mailing,
        zap_api_insert
    )

    logging.info("monitorar_inove >> Aplicacao iniciada!")

    while True:

        agora = datetime.datetime.now().time()
        dia_semana = datetime.datetime.now().strftime("%A").lower()

        try:
            logging.info("monitorar_inove >> Inicio monitoramento do EvenceUra...")

            if (
                dia_semana in periodos_execucao
                and periodos_execucao[dia_semana]["inicio"] <= agora <= periodos_execucao[dia_semana]["fim"]
            ):
                lista_alertas = monitorar_mailing()
                if lista_alertas == None:
                    continue
                elif 'Falha' in lista_alertas:
                    zap_api_insert(
                        mensagem=lista_alertas,
                        agora=agora 
                    )
                else:
                    for alerta in lista_alertas:
                        zap_api_insert(
                            mensagem=alerta,
                            agora=agora
                        )

            logging.info("monitorar_inove >> Fim monitoramento EvenceUra!")
        except Exception as e:
            logging.error(
                f"monitorar_inove >> Erro ao monitorar EvenceUra, detalhes: {str(e)}"
            )

        import time

        time.sleep(30)

        logging.info("monitorar_inove >> Aplicacao finalizada!")
