import pandas as pd

def teste_api_insert(msn):
    import json
    import requests
    api_url = "http://168.121.7.194:5001/api/alertas_insert"
    header = {
        'usuario': 'producao.inove',
        'senha': 'Produc@0',
        'token': r'bhi!!cxrJjzP!-x2L29Jw65AHXMGX7l9pOFg3vAAW6e!n?WhFNWDZd=/1U=L!E?68=0lhV3?UKT6mbCrGrpD?xVH0YOX2-0=3n7GR3o=3Iiep6t6oseWI7Yidhs?HIQ2rIfKC3S?6je1M6nN45RK6M?0bhobg4HhJNbq14zGJ7ILx9g2/9cYVPz8ubWDwukVll5P0ZPlAoJVCtftk4Lj?qHJcqoXMfSe8W2bL=7xFLiLNx1-9f-UeV6SEARp7eZl=yM8RpRUq1-zmT-QV0UWPA0ixwe7LKo4XiNY!BlvaLo=KgGvQJIayMJdyRnRt/h=4SA31CsKFYSGXCSpKijefg!TJRNcP8eU!2a9Uqrx1TkaBSKKXPthDcdUSOdy05rhggmye/jGg8TJ!f?a-whYPdN2gXh-JmBg9XfUQ5be4Nj29NowbkD74h0OZaXKBYfpy9E71ayAPXeQOli=z9B9wxvPRIf9VOniR3CaQ?4NzH-l-JSuLT3TOb?WPaI?FBmqj09caxqCMYb/CnfeXRVL2RhW5K1R7ofUR7tjX/V3LAiKC!T?Kv=rZd6g2VxVZ48LQ!RYA4RE=GvcjDiVFJ=7RCZCXsFSsil1sRfL6=lrvB9zKXHuqIIfRZckLz=UMFlvKG!YO677S!X4tluQS/Dmts0YqaqtNHHTr?hLaRww?!/z20lBik7aNqFtsUwFLFDek=l8efmIXyI90A15U2RuRrzURi0P6bAWYGgg/lPZbHN2PoZlAAdtNJT/3G9F6!WFLxoK!6UQm5Lo7LLHlKJo8zvarZISQEmWB=LAhTKFYhiNNaw-pdqkJq5czIwiFfNPBPU6qamSYM3C7a7LEzdZrmAB5F2OrmzQClqE922kcpfqO/0rUu-O=av=FizbQdFK?gC9tqyuF3h80Sb/tf=C5!Oa5sfqmMepQBn4vDnau-iK3Fi3qIKi612dE2yLnbJ4tDG7q0oRgezAfeYAwE=?1T23F2mu-q1rst1TsbPJP7!y8aS7lEQxPpyYwxEuaqp9WOyW9PxMg-8J/TfwuFtmh=4nPOBtamumY1LQ!32UZSkUSJWNOYIVxtaLTXKztwZi7mz=dD5io1qogl8!EHnz047kc0H3EVayUADap7672X6EOVlmXApOziDP?LgPyWcvET8k/BMoJRojVwkbkDwFK=AEBhxNolCamgwmwk1KtfwU/9t11nJzlJYbWzfXxv6nAjQ7mCXngXhPW/!aL4bMj9U?1J5OCzH?UYQ77SI5RCBbgQsgdX1tQ6sBIp8AnFI?!2kIe/X2zX9c0YFnyN3bS7!fvN!=YMNkiwrE5tn6Ql6CKV0bzI5RQBfw!UCfoWUZvyPC-uf38UsGXAMx71ocQm8XPWP05tab7SsaFvPAg/Vh/2J/YyFjAkX9Ec1dsXsJK1LyuahOGphGe6!Ut5RI-l1dpUCe/xKYn=YlO7Z5wkou6YuFKkFY?aWo5?EpZempDPbe-yHv!6o-P-0QVjejO4K9sEnS-muWHLKmVu2!VAweKnv!XVCvgh7yq95/0aryahsXyt8umiPGwYX/lzdtk4w2dDr8Ul6/dSYadYrblVXZ=sm0GMPB9RhZpDx8nKFyF5/D6g/X6FIuSz25SIv7edBatAihp=o-IO/dZIWdzsY4yZNxQOC-m02r?wC?mImr4jMDLcNBgx!m2UAV8aSAFvqJvufA4usCb35S-xADJ8rz25yG-mZkss3UcjApO!9ghrC0XV2Dh18ArdGNzPKJIBdkqcgYNHRrX3SCAzfErqeLz39qMnlitRP!gTnzSO1?VAqr0kwR7OXvzDwzl/hm1l=NP449GDEUKmyx!w2YErmeqXkHXVS9t?HaB?81cH9Qj466g2GBUtZo?-lX1JV38AWg7OmmBIBkoMyvM24td=5?goM60do0DJ61cx/ah9O1hzgHG/8jTvDcxT2sNgkxQMTSNVpruYjIfFV1W1nXJ94ZyctCM3W1ldnkmS=Vv-t6wGHt79jZp=rn7ekUhE6L271dC93TUrs/Xf6u58mD68RiFxVyqU=MqG7qGPSpNAHE', 
        "Content-Type": "application/json"
    }
    payload = {
        'tipo_alerta': 'monitor',
        'mensagem': msn,
        'status': 'enviado',
        'prioridade': 'baixa',
        'data_criacao': '2024/02/12',
        'data_envio': '',
        'bot_responsavel': 'monitoria_mailing',
    }
    response = requests.request("POST", api_url, headers=header, data=json.dumps(payload))
    print(response)
    print(response.json())

    if response.status_code == 200:
        data = response.json()
        print(data)
        try:
            import json
            data = json.loads(data)
            df = pd.DataFrame(data).fillna('').apply(lambda x: '' if str(x).upper() == 'NAN' or str(x).upper() == 'NONE' else x, axis=1 )
        except Exception as e:
            print(f"Erro ao criar DataFrame: {e}")
            return None
        return df
    else:
        print(f"Falha {response.status_code}:")
        print(response.text)
        return None

def teste_api_select():
    import requests
    import json
    api_url = "http://168.121.7.194:5001/api/alertas_consumo"
    header = {
        'usuario': 'producao.inove',
        'senha': 'Produc@0',
        'token': r'bhi!!cxrJjzP!-x2L29Jw65AHXMGX7l9pOFg3vAAW6e!n?WhFNWDZd=/1U=L!E?68=0lhV3?UKT6mbCrGrpD?xVH0YOX2-0=3n7GR3o=3Iiep6t6oseWI7Yidhs?HIQ2rIfKC3S?6je1M6nN45RK6M?0bhobg4HhJNbq14zGJ7ILx9g2/9cYVPz8ubWDwukVll5P0ZPlAoJVCtftk4Lj?qHJcqoXMfSe8W2bL=7xFLiLNx1-9f-UeV6SEARp7eZl=yM8RpRUq1-zmT-QV0UWPA0ixwe7LKo4XiNY!BlvaLo=KgGvQJIayMJdyRnRt/h=4SA31CsKFYSGXCSpKijefg!TJRNcP8eU!2a9Uqrx1TkaBSKKXPthDcdUSOdy05rhggmye/jGg8TJ!f?a-whYPdN2gXh-JmBg9XfUQ5be4Nj29NowbkD74h0OZaXKBYfpy9E71ayAPXeQOli=z9B9wxvPRIf9VOniR3CaQ?4NzH-l-JSuLT3TOb?WPaI?FBmqj09caxqCMYb/CnfeXRVL2RhW5K1R7ofUR7tjX/V3LAiKC!T?Kv=rZd6g2VxVZ48LQ!RYA4RE=GvcjDiVFJ=7RCZCXsFSsil1sRfL6=lrvB9zKXHuqIIfRZckLz=UMFlvKG!YO677S!X4tluQS/Dmts0YqaqtNHHTr?hLaRww?!/z20lBik7aNqFtsUwFLFDek=l8efmIXyI90A15U2RuRrzURi0P6bAWYGgg/lPZbHN2PoZlAAdtNJT/3G9F6!WFLxoK!6UQm5Lo7LLHlKJo8zvarZISQEmWB=LAhTKFYhiNNaw-pdqkJq5czIwiFfNPBPU6qamSYM3C7a7LEzdZrmAB5F2OrmzQClqE922kcpfqO/0rUu-O=av=FizbQdFK?gC9tqyuF3h80Sb/tf=C5!Oa5sfqmMepQBn4vDnau-iK3Fi3qIKi612dE2yLnbJ4tDG7q0oRgezAfeYAwE=?1T23F2mu-q1rst1TsbPJP7!y8aS7lEQxPpyYwxEuaqp9WOyW9PxMg-8J/TfwuFtmh=4nPOBtamumY1LQ!32UZSkUSJWNOYIVxtaLTXKztwZi7mz=dD5io1qogl8!EHnz047kc0H3EVayUADap7672X6EOVlmXApOziDP?LgPyWcvET8k/BMoJRojVwkbkDwFK=AEBhxNolCamgwmwk1KtfwU/9t11nJzlJYbWzfXxv6nAjQ7mCXngXhPW/!aL4bMj9U?1J5OCzH?UYQ77SI5RCBbgQsgdX1tQ6sBIp8AnFI?!2kIe/X2zX9c0YFnyN3bS7!fvN!=YMNkiwrE5tn6Ql6CKV0bzI5RQBfw!UCfoWUZvyPC-uf38UsGXAMx71ocQm8XPWP05tab7SsaFvPAg/Vh/2J/YyFjAkX9Ec1dsXsJK1LyuahOGphGe6!Ut5RI-l1dpUCe/xKYn=YlO7Z5wkou6YuFKkFY?aWo5?EpZempDPbe-yHv!6o-P-0QVjejO4K9sEnS-muWHLKmVu2!VAweKnv!XVCvgh7yq95/0aryahsXyt8umiPGwYX/lzdtk4w2dDr8Ul6/dSYadYrblVXZ=sm0GMPB9RhZpDx8nKFyF5/D6g/X6FIuSz25SIv7edBatAihp=o-IO/dZIWdzsY4yZNxQOC-m02r?wC?mImr4jMDLcNBgx!m2UAV8aSAFvqJvufA4usCb35S-xADJ8rz25yG-mZkss3UcjApO!9ghrC0XV2Dh18ArdGNzPKJIBdkqcgYNHRrX3SCAzfErqeLz39qMnlitRP!gTnzSO1?VAqr0kwR7OXvzDwzl/hm1l=NP449GDEUKmyx!w2YErmeqXkHXVS9t?HaB?81cH9Qj466g2GBUtZo?-lX1JV38AWg7OmmBIBkoMyvM24td=5?goM60do0DJ61cx/ah9O1hzgHG/8jTvDcxT2sNgkxQMTSNVpruYjIfFV1W1nXJ94ZyctCM3W1ldnkmS=Vv-t6wGHt79jZp=rn7ekUhE6L271dC93TUrs/Xf6u58mD68RiFxVyqU=MqG7qGPSpNAHE', 
        "Content-Type": "application/json"
    }
    response = requests.request("POST", api_url, headers=header)

    if response.status_code == 200:
        data_origem = response.json()
        try:
            import json
            data = json.loads(data_origem)
            df = pd.DataFrame(data)
            return df
        except Exception as e:
            print(f"Erro ao criar DataFrame: {e}")
            return None
    else:
        print(f"Falha {response.status_code}:")
        print(response.text)
        return None

def monitorar_internamente(logging):

    logging.info("monitoria_interna >> inicio")

    try:
        logging.info("monitoria_interna >> tratativa iniciada")

        df = teste_api_select()
        if isinstance(df, pd.DataFrame):
            df = df[df['status'] ==  'pendente']
            lista_alertas = df['mensagem'].to_list()
            if lista_alertas.__len__() > 0:
                for i in lista_alertas:
                    teste_api_insert(str(i))
                return lista_alertas
            else:
                return None

        logging.info("monitoria_interna >> tratativa finalizada")
    except Exception as e:
        logging.error(f"monitoria_interna >> tratativa deu erro: {str(e)}")

    logging.info("monitoria_interna >> final")
    return None
