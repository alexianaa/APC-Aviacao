import csv
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# open abre o arquivo e devolve a arquivo_csv como um objeto de arquivo
# newline='' diz ao interpretador para considerar uma strig vazia como sinal para iniciar uma nova linha.
# do arquivo csv é agrupado em dicionários.
# em dados as informacoes da tabela csv serão lidas e agrupadas em dicionários.
# lembrando que o modelo do dicionário generalizado é {chave: valor}, exemplo: {'peso_decolagem': '100000' }

arquivo_csv = open('database_aeromodelos.csv', newline='')
dados = csv.DictReader(arquivo_csv, delimiter = ',')

# para separar os dados da tabela, foram criadas listas que irão armazenar esses dados.
modelo = []
peso_decolagem = []
comprimento_pista = []
velocidade_aproximacao = []
envergadura = []
distancia_rodas = []
base_rodas = []
distancia_cabine = []
comprimento_fuselagem = []
comprimento_aeronave = []
empenagem = []
passageiros = []

# utilizando o laço de repetição for, pecorre-se cada dado dentro do dicionário dados
# e se a chave for a que queremos, adicionamos o valor dessa chava a lista correspondente, usando o método append()
# o método append() adiciona um único elemento por vez no fim de uma lista
# ao fazer isso, foi utiliado a função float() para transformar o conteúdo do formato string para ponto flutuante ('100000' ----> 100000.00)
# o mesmo vale para o int()

for dado in dados:
    modelo.append(dado['modelo_aeronave'])
    peso_decolagem.append(float(dado['peso_decolagem']))
    comprimento_pista.append(float(dado['comprimento_pista']))
    velocidade_aproximacao.append(float(dado['velocidade_aproximacao']))
    envergadura.append(float(dado['envergadura']))
    distancia_rodas.append(float(dado['distancia_entre_rodas']))
    base_rodas.append(float(dado['base_rodas']))
    distancia_cabine.append(float(dado['distancia_cabine_trem']))
    comprimento_fuselagem.append(float(dado['comprimento_fuselagem']))
    comprimento_aeronave.append(float(dado['comprimento_aeronave']))
    empenagem.append(float(dado['empenagem']))
    passageiros.append(int(dado['capacidade_de_passageiros']))

# essas serão as opções que aparecerão na caixa seletora do filtro
opcoes_filtro = ['Peso de decolagem (kg)',
                'Comprimento de pista (m)',
                'Velocidade de aproximação em nós',
                'Envergadura (m)', 
                'Distância entre rodas (m)', 
                'Base de rodas (m)',
                'Distância da cabine até o trem de pouso principal (m)',
                'Comprimento de fuselagem (m)',
                'Comprimento da aeronave (m)',
                'Empenagem (m)',
                'Capacidade de passageiros']

# essas são as opções e os valores de uma filtragem dos dados que reúne dados dentro de uma faixa de valor
opcoes_zomm_peso = ['Menor que 150', 'Menor que 65 mil', 'Total']
valor_de_opcoes_zomm_peso = ['<150', '<65000', 'Total']


app = dash.Dash(__name__)

# nesse ponto, configurammos a aparência da aplicação que será executada no browser
app.layout = html.Div([
    html.P("Categoria:"),                       # Para o nome 'Categoria' aparecer
    dcc.Dropdown(                               # componente do dash que cria uma caixa seletora
        id="categoria-dropdown",                # id é um componente usado para identificar o componente dash no callback. Precisa ser único
        options=[                               # aqui são definidos as opções da caixa seletora dentro das opções na lista opcoes_filtros
            {'label': opcao, 'value': opcao}    
            for opcao in opcoes_filtro          # esse laço percorre todas as opções dentro da lista opcoes_filtro
        ],
        value = opcoes_filtro[0],               # aqui é definido o valor que aparecerá por padrão na caixa seletora, nesse caso, o valor que será mostrado é aquele da posição 0 da lista opcoes_filtro
        clearable=False,                        # propriedade do componente dropdown que permite limpar o valor selecionado. Determinar False impede isso.
    ),
    dcc.RadioItems(            # componente que cria checkboxes para filtragem de dados                 
        id = "categoria-2",    # identificação do componente para chamada no callback                 
        options = [{'label': opcao, 'value':valor} for opcao, valor in zip(opcoes_zomm_peso, valor_de_opcoes_zomm_peso)],
        value = 'Total'
    ),
    # zip() é uma função que uni dois valores em locais distintos em uma tupla.
    # Ex.:
    #   >>> a = ('Charles', 'Michael', 'Anna')
    #   >>> b = ('June', 'Bia', 'John')
    #   >>> x = zip(a,b)
    #   >>> print(x)
    #   >>> (('Charles', 'June'), ('Michael','Bia'), ('Anna','John'))
    dcc.Graph(id="bar-chart"),  #componente usado para renderizar gráficos plotly
])

# função responsável por filtrar dados com o auxílio de estrutura de decisão if-else
# retorna listas com os dados filtrados
def filtro(opcao, valor):
    valores_filtrados = []
    aeronaves_filtradas = []
    if opcao == 'Peso de decolagem (kg)':
        y = peso_decolagem
    elif opcao == 'Comprimento de pista (m)':
        y = comprimento_pista
    elif opcao == 'Velocidade de aproximação em nós':
        y = velocidade_aproximacao
    elif opcao == 'Envergadura (m)':
        y = envergadura
    elif opcao == 'Distância entre rodas (m)':
        y = distancia_rodas
    elif opcao == 'Base de rodas (m)':
        y = base_rodas
    elif opcao == 'Distância da cabine até o trem de pouso principal (m)':
        y = distancia_cabine
    elif opcao == 'Comprimento de fuselagem (m)':
        y = comprimento_fuselagem
    elif opcao == 'Comprimento da aeronave (m)':
        y = comprimento_aeronave
    elif opcao == 'Empenagem (m)':
        y = empenagem
    elif opcao == 'Capacidade de passageiros':
        y = passageiros

    if valor == '<150':
        for conteudo, aeromodelo in zip(y, modelo):
            if conteudo <= 150:
                valores_filtrados.append(conteudo)
                aeronaves_filtradas.append(aeromodelo)
    elif valor == '<65000':
        for conteudo, aeromodelo in zip(y, modelo):
            if conteudo <= 65000:
                valores_filtrados.append(conteudo)
                aeronaves_filtradas.append(aeromodelo)
    elif valor == 'Total':
        valores_filtrados = y
        aeronaves_filtradas = modelo

    return [valores_filtrados, aeronaves_filtradas]

# app.callbak é um decorador, uma função que recebe parâmetros de entrada e saída e retorna uma função
@app.callback(
    Output("bar-chart", "figure"), 
    [Input("categoria-dropdown", "value"), Input('categoria-2', 'value')]
    )
def grafico_1(argumento, maior_menor):
    dados_filtrados = filtro(argumento, maior_menor)
    eixo_x = dados_filtrados[1]
    eixo_y = dados_filtrados[0]
    barras1 = go.Bar(
        x = eixo_x,
        y = eixo_y,
    )

    grafico = go.Figure(barras1)

    return grafico
# execução do código, debug=True permite ver as mensagens de erro durante a execução da aplicação;
# use_reloader = False desativa o recarregamento do código, o carregamento do código reinicia a aplicação quandoo código é alterado.

if __name__ == '__main__':
    app.run_server(debug = True, use_reloader = False)
