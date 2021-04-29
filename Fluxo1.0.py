#Primeiro a gente importa tudo que vamos esta utilizando
import plotly.graph_objects as go
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
 

def filtro(arquivo):
    if arquivo in 'Fluxo de Passageiros':
        arquivo_csv = "Fluxo - Passageiros.csv"
    elif arquivo in 'Fluxo de Decolagens':
        arquivo_csv = 'Fluxo - Decolagens.csv'
    elif arquivo in 'Fluxo de passageiros por decolagens':
        arquivo_csv = 'Fluxo - Passageiros por Decolagem.csv'
    
    definindo_dados = pd.read_csv(arquivo_csv, quotechar='"')
    data = definindo_dados.values[:,0] 
    gol= definindo_dados.values[:,1]
    tam = definindo_dados.values[:,2]
    azul = definindo_dados.values[:,3]
    avianca = definindo_dados.values[:,4]
    passaredo = definindo_dados.values[:,5]

    return [data,gol,tam,azul,avianca,passaredo]

filtro_fluxo = ['Fluxo de Passageiros',
                'Fluxo de Decolagens',
                'Fluxo de passageiros por decolagens']

#apresentação do gráfico no dash
app = dash.Dash(__name__)
app.layout = html.Div([
    html.P("Categoria:"),                       # Para o nome 'Categoria' aparecer.
    dcc.Dropdown(                               # componente do dash que cria uma caixa seletora
        id="filtro-fluxo",                # id é um componente usado para identificar o componente dash...
                                                # no callback. Precisa ser único.
        options=[      # aqui são definidos as opções da caixa seletora dentro das opções na lista opcoes_filtros
            {'label': opcao, 'value': opcao}    
            for opcao in  filtro_fluxo   # esse laço percorre todas as opções dentro da lista opcoes_filtro
        ],
        value =  filtro_fluxo[0],  # aqui é definido o valor que aparecerá por padrão na caixa seletora.
        clearable=False, # propriedade do componente dropdown que permite limpar o valor selecionado. Determinar False impede isso.
    ),


    dcc.Graph(id = "grafico")  #componente usado para renderizar gráficos plotly
 
])

@app.callback(
    Output(component_id='grafico', component_property= 'figure'),
    Input(component_id='filtro-fluxo', component_property='value'),
)

def gerar_grafico (opcao):
    data,gol,tam,azul,avianca,passaredo = filtro(opcao)

    fig= go.Figure() #nome do gráfico
    #valores do gráfico
    
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



if __name__ == '__main__':
    app.run_server(debug = True, use_reloader = False)