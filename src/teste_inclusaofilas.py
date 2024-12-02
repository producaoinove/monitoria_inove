from settings import dados_uravoz

if __name__ == "__main__":

    dados_uravoz["CONTATOS - NIVA IPBOX"]
    print(dados_uravoz["CONTATOS - NIVA IPBOX"])
    dados_uravoz["CONTATOS - NIVA IPBOX"]["canais"] = 10
    dados_uravoz["CONTATOS - NIVA IPBOX"]["id_lote_rodando"] = 12345
    dados_uravoz["CONTATOS - NIVA IPBOX"]["descricao_lote_rodando"] = "Lote A"
    dados_uravoz["CONTATOS - NIVA IPBOX"]["qtd_trabalhada"] = 200
    dados_uravoz["CONTATOS - NIVA IPBOX"]["qtd_total"] = 500
    dados_uravoz["CONTATOS - NIVA IPBOX"]["id_ultimo_mailing"] = 6789
    dados_uravoz["CONTATOS - NIVA IPBOX"]["arquivo_ultimo_mailing"] = "arquivo_123.csv"
    dados_uravoz["CONTATOS - NIVA IPBOX"]["novos"] = 50
    dados_uravoz["CONTATOS - NIVA IPBOX"]["atualizados"] = 150
    dados_uravoz["CONTATOS - NIVA IPBOX"]["data_ultima_importacao"] = "2024-09-28"

    print(dados_uravoz["CONTATOS - NIVA IPBOX"])
