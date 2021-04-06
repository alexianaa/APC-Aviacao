import csv
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

def carregar_arquivo(arquivo):
    return open(arquivo, newline='')

def obter_dados(arquivo):
    leitor = csv.DictReader(arquivo, delimiter = ',')
    return leitor

arquivo_csv = carregar_arquivo('aeronaves.csv')
dados = obter_dados(arquivo_csv) #dados é um arquivo do tipo DictReader

#dados_dict = dict(next(dados)) #transformando DictReader em Dict
#chaves = list(dados_dict.keys()) #usando o método keys() para obter as chaves dentro de dados_dict e transformando em uma lista
#{chave: valor}
#{modelo_aeronave: a380}

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

#print(sorted(peso_decolagem))
'''
lista1 = ['10.5', '10.5', '10.5', '10.5', '10.6', '10.6', '8.8', '9.1', '9.2', '9.2', '9.2', '9.2', '9.5']
lista2 = []
for i in lista1:
    lista2.append(float(i))
print(sorted(lista2))
'''
#print(modelo, peso_decolagem, comprimento_pista, velocidade_aproximacao, envergadura, distancia_rodas, distancia_cabine, comprimento_fuselagem, comprimento_aeronave, empenagem)

opcoes_filtro = ['Peso de decolagem (kg)',
                'Comprimento de pista (m)',
                'Velocidade de aproximação em nós',
                'Envergadura (m)', 
                'Distância entre rodas (m)', 
                'Base de rodas (m)',
                'Distância da cabine até o trem de pouso principal (m)',
                'Comprimento de fuselagem (m)',
                'Comprimento da aeronave (m)',
                'Empenagem (m)']

opcoes_zomm_peso = ['Maior que 65 mil kg', 'Menor que 65 mil kg', 'Total']
valor_de_opcoes_zomm_peso = ['>65000', '<65000', 'Total']

app = dash.Dash(__name__)

app.layout = html.Div([
    html.P("Categoria:"),
    dcc.Dropdown(
        id="categoria-dropdown",
        options=[
            {'label': opcao, 'value': opcao}
            for opcao in opcoes_filtro
        ],
        value = opcoes_filtro[0],
        clearable=False,
    ),
    dcc.RadioItems(
        id = "categoria-2",
        options = [{'label': opcao, 'value':valor} for opcao, valor in zip(opcoes_zomm_peso, valor_de_opcoes_zomm_peso)],
        value = 'Total'
    ),
    dcc.Graph(id="bar-chart"),
])

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

    if valor == '<65000':
        for peso, aeromodelo in zip(y, modelo):
            if peso <= 65000:
                valores_filtrados.append(peso)
                aeronaves_filtradas.append(aeromodelo)
    elif valor == 'Total':
        valores_filtrados = y
        aeronaves_filtradas = modelo

    return [valores_filtrados, aeronaves_filtradas]

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

'''
def update_output(opcao):
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

    fig = go.Figure(
        data=go.Bar(x=modelo, y=y)
    )
    return fig
'''

app.run_server(debug=True)