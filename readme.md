# Bot Monitoria - Inove

-> Monitoria da Inove, acompanha IPBOX, VONIX, NOSSA_URA

# Estudo do código ( feito em 02/12/2024 )

1 -> Qualidade do código em si:

    - Flak8: Alguns erros de imports, justificados por serem importações de módulos locais.

    - Pylint: Nota 8.45/10, justificados pela presença de erros em importações locais.

    - Radon: 

        > Mantenabilidade:
src\app.py - A
src\teste_inclusaofilas.py - A
src\modules\auxiliar.py - A
src\modules\functions.py - A
src\modules\monitorialeads.py - A
src\modules\monitoriamailing.py - A
src\modules\monitoriavonix.py - A
src\modules\monitor_uravoz.py - A
src\modules\monitor_uravoz2.py - A
src\modules\monitor_urazap.py - A
src\modules\__init__.py - A
src\settings\paths.py - A
src\settings\setup.py - A
src\settings\variables.py - A
src\settings\__init__.py - A

        > Complexidade:
src\modules\auxiliar.py
    F 28:0 acessar_pagina - B
    F 59:0 extrair_tabela_ipbox - A
    F 5:0 criar_navegador - A
src\modules\functions.py
    F 565:0 coletar_dados_ipbox - C
    F 442:0 verifica_tempo_operacao - C
    F 513:0 realizar_login_ipbox - B
    F 257:0 extrair_dados_monitorialeads - B
    F 12:0 realizar_login - B
    F 112:0 extracao_campanha_nossaura - B
    F 366:0 enviar_mensagem - A
    F 66:0 ir_campanha - A
    F 313:0 extracao_monitorialeads - A
    F 158:0 tratar_dados_campanha - A
    F 202:0 pegar_id_fila_monitorialeads - A
    F 347:0 logar_no_whatsapp - A
    F 405:0 post_acompanhamento - A
    F 182:0 pegar_timestamp - A
    F 223:0 construir_url_monitorialeads - A
    F 243:0 formatar_data_hora - A
src\modules\monitorialeads.py
    F 1:0 executar_monitorleads - C
src\modules\monitoriamailing.py
    F 5:0 monitorar_mailing - B
src\modules\monitoriavonix.py
    F 114:0 verifica_tempo_operacao - C
    F 79:0 puxar_informacoes - B
    F 33:0 realizar_login - A
    F 183:0 monitorar_vonix - A
    F 18:0 criar_navegador - A
src\modules\monitor_uravoz.py
    F 4:0 monitorar_uravoz - B
src\modules\monitor_uravoz2.py
    F 4:0 monitorar_uravoz2 - B
src\modules\monitor_urazap.py
    F 4:0 monitorar_urazap - B
src\settings\setup.py
    F 16:0 validar_pastas - A
    F 23:0 validar_pacotes - A
    F 6:0 setup_log - A
src\settings\variables.py
    F 16:0 inicializar_dict_ipbox - A

    - Bandit: Nenhuma vulnerabilidade encontrada.
Test results:
    No issues identified.

Code scanned:
    Total lines of code: 0
    Total lines skipped (#nosec): 0

Run metrics:
    Total issues (by severity):
        Undefined: 0
        Low: 0
        Medium: 0
        High: 0
    Total issues (by confidence):
        Undefined: 0
        Low: 0
        Medium: 0
        High: 0

2 -> Consumo de recursos:

    - psutil: CPU em % | Memória em MB
0 - 0.5 | 30 - 40

    - memory_profiler: 
MEM 1.605469 1733071421.6111
MEM 3.347656 1733071421.7113
MEM 3.347656 1733071421.8120
MEM 3.347656 1733071421.9125
MEM 3.347656 1733071422.0130
MEM 3.347656 1733071422.1136
MEM 3.347656 1733071422.2142
MEM 3.347656 1733071422.3145
MEM 3.347656 1733071422.4152
MEM 3.347656 1733071422.5161