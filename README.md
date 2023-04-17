# FutureCast
O FutureCast é um script em Python que utiliza regressão linear do Scikit-Learn para projetar valores futuros de APIs e aplicativos a partir de um banco de dados SQLite, permitindo uma melhor tomada de decisões e planejamento de operações.


# Introdução:

A previsão de dados futuros é uma tarefa importante em muitos campos, desde finanças e economia até ciência de dados e inteligência artificial. No mundo das APIs e aplicativos, a projeção de valores futuros pode ajudar as empresas a planejar melhor suas operações, aprimorar a tomada de decisões e garantir a qualidade do serviço. Neste contexto, o uso de algoritmos de aprendizado de máquina se tornou cada vez mais comum para fazer projeções precisas e eficientes.

Neste artigo, vamos apresentar o "FutureCast", um script em Python que realiza a projeção de valores futuros para APIs e aplicativos, utilizando um modelo de regressão linear do pacote Scikit-Learn. O script consulta um banco de dados SQLite onde os dados de transações das APIs e aplicativos são armazenados, agrupa esses dados por API, aplicativo, dia da semana e hora do dia e ajusta um modelo de regressão linear para cada API e aplicativo, projetando valores futuros para cada API e aplicativo em cada hora do dia, considerando o dia da semana atual. Em seguida, ele insere as projeções na tabela api_projection do banco de dados.

Com este script, é possível obter projeções precisas e atualizadas dos valores futuros das suas APIs e aplicativos, permitindo que você tome decisões informadas e melhor planeje suas operações. Se você está procurando uma maneira de aprimorar suas projeções de dados futuros, o FutureCast pode ser a solução que você estava procurando. Então chega de enrolação e vamos colocar a mão na massa.

# PRÉ REQUISITOS:
```
**Python 3.8 ou ou superior
Pandas 1.0.0 ou superior
Scikit-Learn 0.22.0 ou superior
SQLite 3.32.3 ou superior**
```
Para instalar as dependências do Python, você pode utilizar o gerenciador de pacotes pip. Basta executar os seguintes comandos em um terminal:
```
 pip install pandas
 pip install scikit-learn
``` 

Para verificar se o SQLite está instalado em seu sistema, você pode digitar "**sqlite3**" no terminal. Se o comando for reconhecido e você for levado para o prompt do SQLite, o SQLite está instalado. Caso contrário, você pode instalar o SQLite de acordo com as instruções do seu sistema operacional.

O banco de dados SQLite deve ser criado e conter uma tabela chamada "**api_summary**" com os seguintes campos: data (texto), application (texto), api (texto) e total (inteiro). A tabela deve conter dados históricos de transações de APIs e aplicativos, para que o FutureCast possa fazer a projeção de valores futuros.

Esse bloco de código executa uma inserção de dados em um banco de dados SQLite, na tabela chamada "**api_summary**". Primeiro, é estabelecida uma conexão com o banco de dados. Em seguida, é definida a data inicial como a data atual, e gerado um intervalo de 30 dias a partir dessa data, com um loop para percorrer cada dia desse intervalo e cada hora do dia. Para cada hora, é gerado um valor aleatório entre 1000 e 10000 para o campo "total". Por fim, esses dados são inseridos na tabela "**api_summary**".

Após a inserção de todos os dados, as alterações são confirmadas (comitadas) e a conexão com o banco de dados é fechada. O objetivo desse bloco de código é gerar dados aleatórios para a tabela "**api_summary**", de modo que o script FutureCast possa fazer a projeção de valores futuros para as APIs e aplicativos a partir desses dados históricos.

O Código fonte está no script insert_fake-data.py deste projeto:

[insert_fake-data.py](https://github.com/leoberbert/FutureCast/blob/main/insert_fake-data.py)

Se quiser inserir dados de outras APIs ou aplicativos na tabela "**api_summary**", você deve alterar o bloco abaixo:
```
cur.execute("INSERT INTO api_summary (data, application, api, total) VALUES (?, ?, ?, ?)", (data_hora_atual.strftime('%Y-%m-%d %H:%M'), 'vivaolinux', '/artigos/v1', total))
```
No comando "INSERT INTO", a primeira coluna especificada é "data", seguida por "application", "api" e "total". Se o usuário desejar inserir dados de outras APIs ou aplicativos, ele deve substituir "vivaolinux" pela aplicação desejada e "/artigos/v1" pela API desejada, e certificar-se de que as colunas "data" e "total" estejam com os valores corretos. Por exemplo:
```
cur.execute("INSERT INTO api_summary (data, application, api, total) VALUES (?, ?, ?, ?)", (data_hora_atual.strftime('%Y-%m-%d %H:%M'), 'meuapp', '/api/v2', total))
```
Nesse exemplo, a aplicação é "meuapp" e a API é "/api/v2". O valor de "total" ainda é gerado aleatoriamente entre 1000 e 10000. É importante lembrar que, ao adicionar novas APIs ou aplicativos, é necessário ajustar o script FutureCast para considerar esses novos dados em suas projeções.

Agora que temos os dados, iremos fazer a projeção.

# Projetando dados Futuros


O primeiro bloco do código importa bibliotecas importantes para o script, como a biblioteca sqlite3 para se conectar ao banco de dados, a biblioteca pandas para manipular os dados, a biblioteca scikit-learn para realizar a regressão linear e a biblioteca logging para registrar eventos e erros.

Em seguida, o script configura o logger para criar logs das atividades da aplicação. Para isso, é criado um objeto logger e é definido o nível do logger como logging.INFO para indicar que o registro deve ser feito apenas em nível de informação. Em seguida, é verificado se a pasta logs já existe e, se não existir, é criada. O nome do arquivo de log é baseado no nome do script e é criado um manipulador de arquivos rotativos para o log, que é configurado para armazenar as mensagens de log diariamente. Por fim, o manipulador de arquivos é adicionado ao logger.

Em seguida, o script se conecta ao banco de dados usando o sqlite3.connect e cria a tabela api_projection se ela ainda não existir. Além disso, são criados índices na tabela api_projection para melhorar a performance das consultas futuras. Em seguida, é feita uma verificação para garantir que a tabela foi criada com sucesso. Se a tabela não existir, o script exibirá uma mensagem de erro e encerrará a execução.

O script itera sobre as 24 horas do dia e faz uma busca na tabela api_summary para realizar a projeção. Para cada hora, é feita uma consulta no banco de dados para obter todos os dados da tabela api_summary que correspondem à hora atual. Se não houver dados para a hora atual, o script exibe uma mensagem de aviso e passa para a próxima hora.

Caso haja dados disponíveis, o script converte a coluna "data" em um objeto datetime e cria uma coluna "valor" para armazenar o valor numérico do campo "total". Em seguida, os dados são agrupados por API, aplicação e a média horária dos valores é calculada para cada API e aplicação. Depois disso, são criadas colunas para o dia da semana e a hora do dia.

O próximo passo é ajustar um modelo de regressão linear para cada API e aplicação e prever os valores futuros para cada API e aplicação. As projeções são armazenadas em um dicionário e, em seguida, inseridas na tabela api_projection do banco de dados.

Por fim, o script fecha a conexão com o banco de dados e registra uma mensagem indicando que a aplicação foi concluída com sucesso. Se ocorrer algum erro ao estabelecer a conexão com o banco de dados, o script exibirá uma mensagem de erro e encerrará a execução.

O Código fonte está no script **FutureCast.py** deste projeto:

[FutureCast.py](https://github.com/leoberbert/FutureCast/blob/main/FutureCast.py)

Perceba que será criado um diretório chamado logs onde o script for executado. O log bem intuivo para ajudar no entendimento:
```
2023-04-14 14:03:07,740 - PID=20208 - INFO - Iniciando a conexão com o banco de dados ...
2023-04-14 14:03:07,742 - PID=20208 - INFO - Realizando busca na tabela api_summary para realizar a projeção...
2023-04-14 14:03:07,754 - PID=20208 - INFO - Inserindo informações na tabela api_projection para a hora: 0
2023-04-14 14:03:07,766 - PID=20208 - INFO - Inserindo informações na tabela api_projection para a hora: 1
2023-04-14 14:03:07,778 - PID=20208 - INFO - Inserindo informações na tabela api_projection para a hora: 2
2023-04-14 14:03:07,790 - PID=20208 - INFO - Inserindo informações na tabela api_projection para a hora: 3
2023-04-14 14:03:07,805 - PID=20208 - INFO - Inserindo informações na tabela api_projection para a hora: 4
2023-04-14 14:03:07,817 - PID=20208 - INFO - Inserindo informações na tabela api_projection para a hora: 5
2023-04-14 14:03:07,829 - PID=20208 - INFO - Inserindo informações na tabela api_projection para a hora: 6
2023-04-14 14:03:07,841 - PID=20208 - INFO - Inserindo informações na tabela api_projection para a hora: 7
2023-04-14 14:03:07,890 - PID=20208 - INFO - Inserindo informações na tabela api_projection para a hora: 8
2023-04-14 14:03:07,911 - PID=20208 - INFO - Inserindo informações na tabela api_projection para a hora: 9
2023-04-14 14:03:07,931 - PID=20208 - INFO - Inserindo informações na tabela api_projection para a hora: 10
2023-04-14 14:03:07,965 - PID=20208 - INFO - Inserindo informações na tabela api_projection para a hora: 11
2023-04-14 14:03:07,987 - PID=20208 - INFO - Inserindo informações na tabela api_projection para a hora: 12
2023-04-14 14:03:08,002 - PID=20208 - INFO - Inserindo informações na tabela api_projection para a hora: 13
2023-04-14 14:03:08,014 - PID=20208 - INFO - Inserindo informações na tabela api_projection para a hora: 14
2023-04-14 14:03:08,048 - PID=20208 - INFO - Inserindo informações na tabela api_projection para a hora: 15
2023-04-14 14:03:08,063 - PID=20208 - INFO - Inserindo informações na tabela api_projection para a hora: 16
2023-04-14 14:03:08,075 - PID=20208 - INFO - Inserindo informações na tabela api_projection para a hora: 17
2023-04-14 14:03:08,103 - PID=20208 - INFO - Inserindo informações na tabela api_projection para a hora: 18
2023-04-14 14:03:08,118 - PID=20208 - INFO - Inserindo informações na tabela api_projection para a hora: 19
2023-04-14 14:03:08,130 - PID=20208 - INFO - Inserindo informações na tabela api_projection para a hora: 20
2023-04-14 14:03:08,141 - PID=20208 - INFO - Inserindo informações na tabela api_projection para a hora: 21
2023-04-14 14:03:08,150 - PID=20208 - INFO - Inserindo informações na tabela api_projection para a hora: 22
2023-04-14 14:03:08,160 - PID=20208 - INFO - Inserindo informações na tabela api_projection para a hora: 23
2023-04-14 14:03:08,163 - PID=20208 - INFO - Aplicação finalizada com sucesso!!!
```
# Validação dos dados

Agora vamos aprender como validar os dados inseridos nas tabelas criadas anteriormente. Para isso, vamos utilizar a biblioteca do Python para SQLite.

Primeiramente, vamos conectar ao banco de dados usando a função connect() da biblioteca. Em seguida, criamos um cursor para executar comandos SQL no banco de dados.

Para selecionar todos os dados da tabela api_summary, utilizamos o comando execute() com a query SELECT * FROM api_summary, e armazenamos os resultados na variável rows. Em seguida, imprimimos os dados da tabela com o comando print() e um loop que percorre todas as linhas da tabela.

Da mesma forma, selecionamos todos os dados da tabela api_projection, imprimimos os dados e, por fim, fechamos a conexão com o banco de dados utilizando a função close().

Para validar os dados inseridos, você pode alterar as queries de acordo com a sua necessidade, selecionando apenas os campos e tabelas que deseja analisar. O importante é garantir que os dados estejam coerentes e não tenham erros ou inconsistências.

**Código Fonte:**

```
import sqlite3

# Conectar-se ao banco de dados
conn = sqlite3.connect('api_data.db')

# Criar cursor
cur = conn.cursor()

# Selecionar todos os dados da tabela api_summary
cur.execute("SELECT * FROM api_summary")
rows = cur.fetchall()

# Imprimir os dados da tabela api_summary
print("Dados da tabela api_summary:")
for row in rows:
    print(row)

# Selecionar todos os dados da tabela api_projection
cur.execute("SELECT * FROM api_projection")
rows = cur.fetchall()

# Imprimir os dados da tabela api_projection
print("
Dados da tabela api_projection:")
for row in rows:
    print(row)

# Fechar a conexão com o banco de dados
conn.close()
```
Caso queira utilizar alguma IDE compatível com Linux para realizar a validação dos dados, seguem algumas que poderão ser baixadas e instaladas:

1. **SQLiteStudio** - uma ferramenta multiplataforma com interface gráfica para gerenciamento de bancos de dados SQLite.

2. **DB Browser for SQLite** - um aplicativo de código aberto e multiplataforma para gerenciamento de bancos de dados SQLite com interface gráfica.

3. **DBeaver** - uma IDE de banco de dados gratuita e de código aberto com suporte para SQLite, MySQL, PostgreSQL e outros bancos de dados populares.

4. **Sqliteman** - uma IDE de banco de dados SQLite de código aberto com uma interface gráfica de usuário fácil de usar.

5. **SQLite Manager** - uma extensão do Firefox que permite gerenciar bancos de dados SQLite em um navegador

# Visualização dos dados:

Agora vamos à parte mais interessante: visualizar os dados. Para isso, é necessário ter o Grafana instalado no sistema. Além disso, o plugin frser-sqlite-datasource precisa ser instalado. Ele pode ser baixado a partir do link abaixo, onde também estão disponíveis as instruções passo a passo para a instalação:

[grafana-sqlite-datasource](https://github.com/fr-ser/grafana-sqlite-datasource/releases)

Primeiramente, vamos adicionar o datasource do SQLite ao Grafana conforme demonstrado na imagem abaixo:

![IMG01](https://user-images.githubusercontent.com/16724862/232487218-6888e60d-d24f-4025-b875-639d71c35c8c.jpg)

Na tela seguinte, você irá localizar o arquivo api_data.db que foi criado nas execuções anteriores:

![IMG02](https://user-images.githubusercontent.com/16724862/232487306-184ef598-6676-41d6-9a50-af4903fd6627.jpg)

Feito o passo acima, basta clicar no botão "save & test".

Agora vamos criar nosso tão esperado dashboard que irá nos mostrar os dados tanto do passado quanto do futuro para que possamos acompanhar se os mesmos são coerentes:

![IMG03](https://user-images.githubusercontent.com/16724862/232487392-d27fa4a7-145e-443e-9c02-9775739944cc.jpg)

Vamos adicionar um painel do tipo "Time Series":

![IMG05](https://user-images.githubusercontent.com/16724862/232487485-bdf3cbf8-5d60-4412-a6a4-a4ed7f81b2be.jpg)

Em seguida, selecionaremos o datasource que criamos anteriormente e criaremos algumas variáveis para que o uso fique mais dinâmico:

![IMG06](https://user-images.githubusercontent.com/16724862/232487635-2fc87f94-51b7-4399-84dc-495189f74ae9.jpg)

Agora que as coisas começam a ficar mais interessantes, iremos personalizar nossa variável, conforme mostrado abaixo:

![IMG07](https://user-images.githubusercontent.com/16724862/232487757-cfaeee9c-7b00-4138-a3e4-4da64dac5e37.jpg)

![IMG08](https://user-images.githubusercontent.com/16724862/232487916-def1c564-2c0c-4d9e-9912-637e75a6c351.jpg)

Perceba que a variável "api" depende da variável application e deverão estar na seguinte ordem:

![IMG09](https://user-images.githubusercontent.com/16724862/232488001-406db8a4-daf8-423c-9d39-aa4f7d333711.jpg)

Agora, salvaremos nosso dashboard:

![IMG10](https://user-images.githubusercontent.com/16724862/232488080-fce21b63-581e-49ff-b02b-cf5f7783a7e3.jpg)

![IMG11](https://user-images.githubusercontent.com/16724862/232488240-d59d9e5d-7f51-4418-bd07-e85bfe1d0b73.jpg)

Perceba que as variáveis que foram adicionadas já estarão disponíveis para uso:

![IMG12](https://user-images.githubusercontent.com/16724862/232488278-797b10d0-e0ae-4de8-a212-d67b3e56a497.jpg)

Agora, vamos editar nosso gráfico e inserir nossa query:

![IMG13](https://user-images.githubusercontent.com/16724862/232488355-08599a77-dcfc-4890-9db3-c40b8fb95e9e.jpg)

Inseriremos duas queries, sendo a query A para o dado futuro e a query B para o dado do passado. Mantivemos o dado passado no gráfico para ser possível visualizar o comportamento no qual foi baseado o cáculo para projeção do futuro.

![IMG14](https://user-images.githubusercontent.com/16724862/232488488-6a713ac4-3e46-47c8-b889-5d018f17db2c.jpg)

**Query A:**
```
SELECT
strftime('%Y-%m-%dT%H:%M:%SZ', data) as time,
total as projetado
FROM api_projection
WHERE api = '$api' AND application = '$application'
ORDER BY data
```
**Query B:**
```
SELECT
strftime('%Y-%m-%dT%H:%M:%SZ', data) as time,
total as historic
FROM api_summary
WHERE api = '$api' AND application = '$application'
ORDER BY data
```
Perceba que estamos utilizando as variáveis que criamos anteriormente para que, à medida que você selecione sua aplicação e sua API/serviço, o gráfico seja alterado de forma dinâmica.

Por fim, salvaremos nosso dashboard e verificaremos como os dados foram projetados.

![IMG15](https://user-images.githubusercontent.com/16724862/232488870-6a398257-2490-4fe8-a183-fe1a6bd5b241.jpg)

Agora, você pode selecionar o período e ver o comportamento do gráfico:

![IMG16](https://user-images.githubusercontent.com/16724862/232488993-a8e1817c-f919-492d-88eb-16ab3366f5ba.jpg)

É importante ressaltar que, como utilizamos um script que insere dados de forma aleatória, a precisão pode ser impactada.
