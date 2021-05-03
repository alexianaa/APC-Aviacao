import csv
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
from funcoes import *

#dados para o grafico de pizza de acidentes 
tes = pd.read_excel(r"outros.xlsx")
dados = tes.values
categoria_1 = dados[:,0]
valor_1 = dados[:,1]
categoria_2 = dados[:,2]
valor_2 = dados[:,3]

#opcoes para a caixa seletora de fluxo
filtro_fluxo = ['Fluxo de Passageiros',
                'Fluxo de Decolagens',
                'Fluxo de passageiros por decolagens']

#opcoes para a caixa seletora de aeromodelos
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

#opcoes para os seletores de valores de aeronaves
opcoes_de_ampliacao = ['Capacidade de passageiros menor que 150 assentos', 'Peso de decolagem menor que 65 mil kg', 'Total']
valor_de_ampliacao = ['<150', '<65000', 'Total']

#opcoes para a caixa seletora de acidentes
opcoes = ["SP", "RS", "MT", "PA", "PR", "MG", "GO", "MS", "AM", "BA", "SC", "MA", "RR", "RJ","TO", "PI", "PE", "CE", "AC", "ES", "AL", "AP", "RO", "SE", "DF", "INDEFINIDO", "PB", "RN"]

#geração dos graficos em pizza de acidentes
fig_1 = go.Figure()
fig_1.add_trace(go.Pie(values = valor_1, labels = categoria_1))
fig_1.update_layout(title='TIPOS DE ACIDENTES')

fig_2 = go.Figure()
fig_2.add_trace(go.Pie(values = valor_2, labels = categoria_2))
fig_2.update_layout(title='INCIDENTES GRAVES')

#iniciando o dash
app = dash.Dash(__name__)

app.layout = html.Div([

    #primeira parte do dash: grafico de aeronaves com...
    html.Div('Modelos de aeronaves e suas especificações técnicas', style={'color': 'grey', 'fontSize': 30}),

    html.P("Categoria Técnica:"),  

    #...caixa seletora...
    dcc.Dropdown(                                          
        id="dropdown-aeronaves",              
        options=[                                
            {'label': opcao, 'value': opcao}     
            for opcao in opcoes_filtro        
        ],
        value = opcoes_filtro[0],             
        clearable=False,                       
    ),

    #...seletor de valores...
    dcc.RadioItems(                           
        id = "RadioItems-aeronaves",                   
        options = [{'label': opcao, 'value':valor} for opcao, valor in zip(opcoes_de_ampliacao, valor_de_ampliacao)],
        value = 'Total'
    ),

    #geracao do grafico
    dcc.Graph(id="grafico-barras-aeronaves"),

    #segunda parte do dash: grafico de acidentes...
    html.Div('Acidentes aéreos', style={'color': 'grey', 'fontSize': 30}),

    html.P("Unidade da Federação:"),

    #...caixa seletora...
    dcc.Dropdown( 
        id = "dropdown-acidentes",
        options = [{'label': nome, 'value':nome} for nome in opcoes], 
        value = "SP",
        clearable = False
    ),

    #geracao dos graficos: barras, pizza e pizza respectivamente
    dcc.Graph(id = "grafico-barras-acidentesUF"), 
    dcc.Graph(figure = fig_1), 
    dcc.Graph(figure = fig_2), 

    #caixa seletora de fluxo de viagens
    dcc.Dropdown(                            
        id="filtro-fluxo",                
        options=[     
            {'label': opcao, 'value': opcao}    
            for opcao in filtro_fluxo   
        ],
        value = filtro_fluxo[0],  
        clearable=False, 
    ),

    #geracao do grafico def fluxo de viagens
    dcc.Graph(id = "grafico-fluxo") 
 
])

#decorador, uma função que recebe parâmetros de entrada e saída e retorna uma função
@app.callback(
    Output("grafico-barras-aeronaves", "figure"),
    Input("dropdown-aeronaves", "value"),
    Input('RadioItems-aeronaves', 'value')
)

#para selecionar os dados e formar o grafico de cada opcao da caixa seletora de aeronaves
def grafico_aeronaves(argumento, maior_menor):
    dados_filtrados = filtro_aeromodelos(argumento, maior_menor)
    eixo_x = dados_filtrados[1]
    eixo_y = dados_filtrados[0]

    aeronaves_bar = go.Bar(
        x = eixo_x,
        y = eixo_y,
    )

    grafico_aeronaves_bar = go.Figure(aeronaves_bar)
    grafico_aeronaves_bar.update_layout(
        title = dict(
            text = "Especificações técnicas por modelo de aeronave",
            font = dict(
                family = "Arial",
                size = 20,
                color = "grey"
            ),
            xref = "paper",
            yref = "container",
            x = 0.5,
            y = 0.9
        ),
        plot_bgcolor = "snow",
    )
    return grafico_aeronaves_bar

@app.callback(
    Output("grafico-barras-acidentesUF", "figure"),
    Input("dropdown-acidentes", 'value')
)

#para selecionar os dados e formar o grafico de cada opcao da caixa seletora de acidentes
def grafico_acidentesUF(argumento): 
    dados_filtrados = filtro_acidentesUF(argumento) 
    eixo_x = ano
    eixo_y = dados_filtrados
    
    acidentesUF_bar = go.Bar( 
        x = eixo_x,
        y = eixo_y,
    )

    grafico_acidentesUF_bar = go.Figure(acidentesUF_bar) 
    grafico_acidentesUF_bar.update_layout( 
        title = dict( 
            text = "Quantidade de acidentes x anos", 
            font = dict( 
                family = "Arial",
                size = 20,
                color = "gray"),
            xref = "paper", 
            yref = "container", 
            x = 0.5, 
            y = 0.9 
        ),
        plot_bgcolor = "snow", 
    )
    return grafico_acidentesUF_bar 

@app.callback(
    Output(component_id='grafico-fluxo', component_property= 'figure'),
    Input(component_id='filtro-fluxo', component_property='value'),
)

#para selecionar os dados e formar o grafico de cada opcao da caixa seletora de fluxo de viagens
def gerar_grafico (opcao):
    data,gol,tam,azul,avianca,passaredo = filtro(opcao)

    fig= go.Figure() 
    fig.add_trace(go.Scatter(x= data,
                            y= gol,
                            mode='lines',
                            name= 'GOL',
                            line=dict(color="orange")))
    fig.add_trace(go.Scatter(x = data,
                            y = tam,
                            mode ='lines',
                            name = 'TAM',
                            line =dict(color="red")))
    fig.add_trace(go.Scatter(x = data,
                            y = azul,
                            mode='lines',
                            name= 'AZUL',
                            line=dict(color="blue")))
    fig.add_trace(go.Scatter(x = data,
                            y = avianca,
                            mode='lines',
                            name= 'AVIANCA',
                            line=dict(color="darkred")))
    fig.add_trace(go.Scatter(x = data,
                            y = passaredo,
                            mode='lines', 
                            name= 'PASSAREDO', 
                            line=dict(color="yellow")))
    fig.update_layout(title= opcao,
                        xaxis_title='Mês', 
                        yaxis_title='Quantidade')


    return fig

# Executando a aplicação no servidor local
if __name__ == '__main__':
    app.run_server(debug = True, use_reloader = False)