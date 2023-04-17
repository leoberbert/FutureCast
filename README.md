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

