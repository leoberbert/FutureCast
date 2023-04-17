# -*- coding: utf-8 -*-
#=============================================================
# Created: Wed 12 Apr 2023 05:02:30 PM -03
# Modified: Wed 12 Apr 2023 05:02:30 PM -03
# Autor: Leonardo Berbert Gomes
# Description:
# The FutureCast script performs the projection of future values 
# of a specific metric for specified APIs and applications, using a 
# linear regression model. The script queries a SQLite database where 
# the transaction data for the APIs and applications are stored, 
# and groups this data by API, application, day of the week, and 
# hour of the day. Then, it fits a linear regression model 
# for each API and application and projects future values for 
# each API and application at each hour of the day, considering the current day of the week. 
# Finally, it inserts the projections into the api_projection table of the database.
#=============================================================

import warnings,sqlite3,os,datetime,logging,sys
warnings.filterwarnings('ignore', message='X does not have valid feature names')
import pandas as pd
from sklearn.linear_model import LinearRegression
from logging.handlers import TimedRotatingFileHandler

# Configurar o logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Criar a pasta de logs, caso ela não exista
if not os.path.exists('logs'):
    os.mkdir('logs')

# Definir o nome do arquivo de log, baseado no nome do script
log_file = os.path.join('logs', os.path.splitext(os.path.basename(__file__))[0] + '.log')

# Configurar o manipulador de arquivos rotativos por dia
file_handler = TimedRotatingFileHandler(log_file, when='d', interval=1, backupCount=30, encoding='utf-8')
file_handler.setLevel(logging.INFO)

# Configurar o formato da mensagem de log
formatter = logging.Formatter('%(asctime)s - PID=%(process)d - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Adicionar o manipulador de arquivos ao logger
logger.addHandler(file_handler)

# Conectar-se ao banco de dados
try:
    conn = sqlite3.connect('api_data.db')
    logger.info(f'Iniciando a conexão com o banco de dados ...')
    # Criar tabela api_projection
    conn.execute('''CREATE TABLE IF NOT EXISTS api_projection (
                        data TEXT,
                        application TEXT,
                        api TEXT,
                        total INTEGER
                    )''')
    conn.execute('''
    CREATE INDEX IF NOT EXISTS idx_data_projection ON api_projection (data)
    ''')

    conn.execute('''
    CREATE INDEX IF NOT EXISTS idx_api_projection ON api_projection (api)
    ''')

    conn.execute('''
    CREATE INDEX IF NOT EXISTS idx_application_projection ON api_projection (application)
    ''')
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='api_projection';")
    table_exists = cursor.fetchone() is not None
    if not table_exists:
        logger.error("Não foi possível criar a tabela api_projection.")
        sys.exit(1)

    # Iterar sobre todas as horas do dia
    logger.info("Realizando busca na tabela api_summary para realizar a projeção...")
    for hour in range(24):
        # Selecionar os dados da tabela de transações para a próxima hora
        query = f"""SELECT strftime('%Y-%m-%d %H:%M', data) as data, application, api, total
                    FROM api_summary
                    WHERE strftime('%H', data) = '{hour:02}'"""

        df = pd.read_sql_query(query, conn)

        # Verificar se o DataFrame está vazio
        if df.empty:
            logger.warning(f'Não existem dados para realizar a projeção para a hora {hour:02}:00:00.')
            continue

        # Converter a coluna "data" em um objeto datetime e criar uma coluna "valor" para armazenar o valor numérico do "total"
        df['data'] = pd.to_datetime(df['data'], format='%Y-%m-%d %H:%M')
        df['valor'] = pd.to_numeric(df['total'])

        # Agrupar os dados por API, aplicação e calcular a média horária dos valores para cada API e aplicação
        df_por_api_e_aplicacao = df.groupby(['api', 'application', 'data'])['valor'].mean().reset_index()

        # Criar colunas para o dia da semana e hora do dia
        df_por_api_e_aplicacao['dia_da_semana'] = df_por_api_e_aplicacao['data'].dt.dayofweek
        df_por_api_e_aplicacao['hora_do_dia'] = df_por_api_e_aplicacao['data'].dt.hour

        # Ajustar um modelo de regressão linear para cada API e aplicação e prever os valores futuros para cada API e aplicação
        projecoes = {}
        for api in df_por_api_e_aplicacao['api'].unique():
            for application in df_por_api_e_aplicacao['application'].unique():
                df_api_e_aplicacao = df_por_api_e_aplicacao[(df_por_api_e_aplicacao['api'] == api) & (df_por_api_e_aplicacao['application'] == application)]
                if not df_api_e_aplicacao.empty:
                    regressor = LinearRegression()
                    X = df_api_e_aplicacao[['hora_do_dia', 'dia_da_semana']]
                    y = df_api_e_aplicacao['valor']
                    regressor.fit(X, y, sample_weight=None)
                    valor_projetado = regressor.predict([[hour, datetime.datetime.now().weekday()]])
                    projecoes[(api, application)] = valor_projetado[0]  
    # Inserir as projeções na tabela api_projection do banco de dados
        logger.info(f'Inserindo informações na tabela api_projection para a hora: {hour}')
        cursor = conn.cursor()
        for api, application in projecoes.keys():
            valor_projetado_int = int(round(projecoes[(api, application)]))
            data_projecao = datetime.datetime.now().replace(hour=hour, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d %H:%M')
            cursor.execute("INSERT INTO api_projection (data, application, api, total) VALUES (?, ?, ?, ?)", (data_projecao, application, api, valor_projetado_int))
            conn.commit()
    # Fechar a conexão com o banco de dados
    conn.close()
    logger.info(f'Aplicação finalizada com sucesso!!!')
except sqlite3.Error:
    logger.error("Não foi possível estabelecer a conexão com o banco de dados.")
    sys.exit(1)
