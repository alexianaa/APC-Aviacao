import dash
import plotly.graph_objects as go
import pandas as pd
import dash_core_components as dcc 
import dash_html_components as html
from dash.dependencies import Input, Output

#%matplotlib inline

dados = pd.read_csv('Dados_aeromodelos.csv', encoding='UTF-8', sep=';')
#dados do eixo x:
eixo_x = dados.values[:,0] 

#dados diferentes do eixo y:
peso = dados.values[:,1] 
codigo = dados.values[:,2]
comp_pista = dados.values[:,4]
velocidade = dados.values[:,5]
envergadura = dados.values[:,6]
distancia_1 = dados.values[:,7]
base = dados.values[:,8]
distancia_2 = dados.values[:,9]
fuselagem = dados.values[:,10]
comp_aeronave = dados.values[:,11]
empenhagem = dados.values[:,12]
capacidade = dados.values[:,13]

print(capacidade)
# opções para o filtro
opcoes = ["Peso de decolagem", 
        "Comprimento básico de pista de aeronave",
        "Velocidade de aproximação", 
        "Envergadura", 
        "Distância entre Rodas Externas do Trem de Pouso Principal", 
        "Base de rodas", 
        "Distância da cabine do piloto até o trem de pouso principal", 
        "Comprimento da Fuselagem",
        "Comprimento da Aeronave", 
        "Empenagem [Altura da Cauda]", 
        "Capacidade de Passageiros"]

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id = "filtro",
        options = [{'label': nome, 'value':nome} for nome in opcoes],
        value = 'Capacidade de Passageiros',
        placeholder="Selecione uma categoria",
        clearable = False
    ),
    dcc.Graph(id = "grafico"),
])

def separa_dados(nome):
    if nome == "Peso de decolagem":
        eixo_y = peso
    elif nome == "Comprimento básico de pista de aeronave":
        eixo_y = comp_pista
    elif nome == "Velocidade de aproximação":
        eixo_y = velocidade
    elif nome == "Envergadura":
        eixo_y = envergadura
    elif nome == "Distância entre Rodas Externas do Trem de Pouso Principal":
        eixo_y = distancia_1
    elif nome == "Base de rodas":
        eixo_y = base
    elif nome == "Distância da cabine do piloto até o trem de pouso principal":
        eixo_y = distancia_2
    elif nome == "Comprimento da Fuselagem":
        eixo_y = fuselagem
    elif nome == "Comprimento da Aeronave":
        eixo_y = comp_aeronave
    elif nome == "Empenagem [Altura da Cauda]":
        eixo_y = empenhagem
    elif nome == "Capacidade de Passageiros":
        eixo_y = capacidade
    return eixo_y

@app.callback(
    Output(component_id='grafico', component_property= 'figure'),
    [Input(component_id='filtro', component_property='value')]
    )

def grafico_1(argumento):
    linha1 = go.Bar( 
        x = eixo_x,
        y = separa_dados(argumento),
    )

    grafico = go.Figure(linha1)

    return grafico


if __name__ == '__main__':
    app.run_server(debug = True, use_reloader = False)