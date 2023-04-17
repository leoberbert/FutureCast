import sqlite3
import pandas as pd
import random
from datetime import datetime, timedelta

# conectando ao banco de dados
conn = sqlite3.connect('api_data.db')

# criando cursor
cur = conn.cursor()

# definindo data inicial como 30 dias atrás da data atual
data_atual = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
data_inicial = data_atual - timedelta(days=29)

# gerando intervalo de datas dos últimos 30 dias
intervalo_datas = pd.date_range(data_inicial, data_atual, freq='H')

# loop para gerar e inserir dados na tabela api_summary
for data_hora_atual in intervalo_datas:
    # gerando valor aleatório para o campo total
    total = random.randint(1000, 10000)
    
    # inserindo dados na tabela api_summary
    cur.execute("INSERT INTO api_summary (data, application, api, total) VALUES (?, ?, ?, ?)", (data_hora_atual.strftime('%Y-%m-%d %H:%M:%S'), 'vivaolinux', '/artigos/v1', total))

# commitando alterações
conn.commit()

# fechando conexão
conn.close()
