import pandas as pd
from questdb.ingress import Sender
from datetime import datetime, timezone

conf = f'http::addr=questdb:9000;'

tabela = pd.read_csv('./questdb-usuarios-dataset.csv', sep=",")

def inserir_dados():
    try:
        print("Iniciando a inserção dos dados.")
        with Sender.from_conf(conf) as sender:
            print("Inserindo dados!")
            for _, row in tabela.iterrows():
                status_bool = True if row['statusCliente'] == 1 else False
                conexao_inicial = datetime.strptime(row['conexaoInicial'], '%Y-%m-%dT%H:%M:%S.%fZ') if pd.notna(row['conexaoInicial']) else None
                conexao_final = datetime.strptime(row['conexaoFinal'], '%Y-%m-%dT%H:%M:%S.%fZ') if pd.notna(row['conexaoFinal']) else None
                sender.row(
                    'dados',
                    columns={
                        "statusCliente": status_bool,
                        "ipConcentrador": str(row['ipConcentrador']),
                        "nomeConcentrador": str(row['nomeConcentrador']),
                        "latitudeCliente": str(row['latitudeCliente']),
                        "longitudeCliente": str(row['longitudeCliente']),
                        "conexaoInicial": conexao_inicial,
                        "conexaoFinal": conexao_final,
                        "tempoConectado": int(row['tempoConectado']),
                        "consumoDownload": int(row['consumoDownload']),
                        "consumoUpload": int(row['consumoUpload']),
                        "motivoDesconexao": str(row['motivoDesconexao']) if pd.notna(row['motivoDesconexao']) else None,
                        "nomeCliente": str(row['nomeCliente']),
                        "popCliente": str(row['popCliente']) if pd.notna(row['popCliente']) else None,
                        "enderecoCliente": str(row['enderecoCliente']),
                        "bairroCliente": str(row['bairroCliente']),
                        "cidadeCliente": str(row['cidadeCliente']),
                        "planoContrato": str(row['planoContrato']),
                        "statusInternet": int(row['statusInternet']),
                        "valorPlano": float(row['valorPlano']),
                        "timestamp": row['timestamp']
                    },
                    at=datetime(
                            2022, 3, 8, 18, 53, 57, 609765,
                            tzinfo=timezone.utc)
                )
                sender.flush()
            print("Dados inseridos com sucesso!")
    except Exception as erro:
        print(f"Ocorreu um erro: {erro}")
inserir_dados()