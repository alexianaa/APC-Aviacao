import csv
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

################################################################## MODELO DE AERONAVES ##################################################################
# Abertura e leitura da base de dados de aernonaves
arquivo_csv = open('database_aeromodelos.csv', newline='')
dados = csv.DictReader(arquivo_csv, delimiter = ',')

# Criação das listas de características que receberão os dados 
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

# Atribuição dos dados às listas
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


################################################################## ACIDENTES AÉREOS ##################################################################
# Leitura da base de dados de acidentes aéreos
tes = pd.read_excel(r"estados.xlsx")
dados = tes.values

# Criação de listas das Unidades Federativas e atribuição de dados às listas 
ano = dados[:,0]
SP = dados[:,1]
RS = dados[:,2]
MT = dados[:,3]
PA = dados[:,4]
PR = dados[:,5]
MG = dados[:,6]
GO = dados[:,7]
MS = dados[:,8]
AM = dados[:,9]
BA = dados[:,10]
SC = dados[:,11]
MA = dados[:,12]
RR = dados[:,13]
RJ = dados[:,14]
TO = dados[:,15]
PI = dados[:,16]
PE = dados[:,17]
CE = dados[:,18]
AC = dados[:,19]
ES = dados[:,20]
AL = dados[:,21]
AP = dados[:,22]
RO = dados[:,23]
SE = dados[:,24]
DF = dados[:,25]
INDEFINIDO = dados[:,26]
PB = dados[:,27]
RN = dados[:,28]

# Leitura da base de dados da natureza e categoria dos acidentes
tes = pd.read_excel(r"outros.xlsx")
dados = tes.values

# Criação das listas e atribuição de dados às listas
categoria_1 = dados[:,0]
valor_1 = dados[:,1]
categoria_2 = dados[:,2]
valor_2 = dados[:,3]


################################################################## FLUXO DE PASSAGEIROS E DECOLAGENS ##################################################################
# Leitura da base de dados de fluxo de passageiros
def filtro(arquivo):
    if arquivo in 'Fluxo de Passageiros':
        arquivo_csv = "Fluxo - Passageiros.csv"
    elif arquivo in 'Fluxo de Decolagens':
        arquivo_csv = 'Fluxo - Decolagens.csv'
    elif arquivo in 'Fluxo de passageiros por decolagens':
        arquivo_csv = 'Fluxo - Passageiros por Decolagem.csv'
    
    definindo_dados = pd.read_csv(arquivo_csv, quotechar='"')
    data = definindo_dados.values[:,0] 
    #print(data)
    gol= definindo_dados.values[:,1]
    tam = definindo_dados.values[:,2]
    azul = definindo_dados.values[:,3]
    avianca = definindo_dados.values[:,4]
    passaredo = definindo_dados.values[:,5]

    return [data,gol,tam,azul,avianca,passaredo]

filtro_fluxo = ['Fluxo de Passageiros',
                'Fluxo de Decolagens',
                'Fluxo de passageiros por decolagens']


################################################################## FILTRAGEM DE DADOS -> LISTAS DE METADADOS ##################################################################
# Metadados de Modelo de Aeronaves
#   -> características das aeronaves
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

#   -> ampliação de valores
opcoes_de_ampliacao = ['Capacidade de passageiros menor que 150 assentos', 'Peso de decolagem menor que 65 mil kg', 'Total']
valor_de_ampliacao = ['<150', '<65000', 'Total']

# Metadados de Acidentes Aéreos
#   -> Unidades da Federação
opcoes = ["SP", "RS", "MT", "PA", "PR", "MG", "GO", "MS", "AM", "BA", "SC", "MA", "RR", "RJ","TO", "PI", "PE", "CE", "AC", "ES", "AL", "AP", "RO", "SE", "DF", "INDEFINIDO", "PB", "RN"]


################################################################## CRIANDO GRÁFICOS ##################################################################
# criação do gráfico de fluxo de passageiros


# criação do gráficos da natureza e categoria de acidentes
fig_1 = go.Figure()
fig_1.add_trace(go.Pie(values = valor_1, labels = categoria_1))
fig_1.update_layout(title='TIPOS DE ACIDENTES')

fig_2 = go.Figure()
fig_2.add_trace(go.Pie(values = valor_2, labels = categoria_2))
fig_2.update_layout(title='INCIDENTES GRAVES')


################################################################## DASH ##################################################################
app = dash.Dash(__name__)

# Configuração de Layout
app.layout = html.Div([
    #MODELOS DE AERONAVES
    html.Div('Modelos de aeronaves e suas especificações técnicas', style={'color': 'grey', 'fontSize': 30}),
    html.P("Categoria Técnica:"),                       
    dcc.Dropdown(                  # componente do dash que cria uma caixa seletora                          
        id="dropdown-aeronaves",       # id é um componente usado para identificar o componente dash...        
        options=[          # aqui são definidos as opções da caixa seletora dentro das opções na lista opcoes_filtros                       
            {'label': opcao, 'value': opcao}     
            for opcao in opcoes_filtro      # esse laço percorre todas as opções dentro da lista opcoes_filtro    
        ],
        value = opcoes_filtro[0],     # aqui é definido o valor que aparecerá por padrão na caixa seletora.         
        clearable=False,     # propriedade do componente dropdown que permite limpar o valor selecionado. So que nesse caso ele so vai limpar
        #o usuario mudar de opção                   
    ),
    dcc.RadioItems(               # componente que cria checkboxes para filtragem de dados              
        id = "RadioItems-aeronaves",                   
        options = [{'label': opcao, 'value':valor} for opcao, valor in zip(opcoes_de_ampliacao, valor_de_ampliacao)],
        value = 'Total'
    ),
    dcc.Graph(id="grafico-barras-aeronaves"),

    # ACIDENTES AÉREOS OCORRIDOS POR ESTADO
    html.Div('Acidentes aéreos', style={'color': 'grey', 'fontSize': 30}),
    html.P("Unidade da Federação:"),
    dcc.Dropdown( 
        id = "dropdown-acidentes",
        options = [{'label': nome, 'value':nome} for nome in opcoes], 
        value = "SP",
        clearable = False
    ),
    dcc.Graph(id = "grafico-barras-acidentesUF"), #acidentes
    dcc.Graph(figure = fig_1), #acidentes
    dcc.Graph(figure = fig_2), #acidentes

    #FLUXO DE PASSAGEIROS
    dcc.Dropdown(                               # componente do dash que cria uma caixa seletora
        id="filtro-fluxo",                # id é um componente usado para identificar o componente dash...
                                                # no callback. Precisa ser único.
        options=[      # aqui são definidos as opções da caixa seletora dentro das opções na lista opcoes_filtros
            {'label': opcao, 'value': opcao}    
            for opcao in filtro_fluxo   # esse laço percorre todas as opções dentro da lista opcoes_filtro
        ],
        value = filtro_fluxo[0],  # aqui é definido o valor que aparecerá por padrão na caixa seletora.
        clearable=False, # propriedade do componente dropdown que permite limpar o valor selecionado. Determinar False impede isso.
    ),


    dcc.Graph(id = "grafico")  #componente usado para renderizar gráficos plotly
 
])


# FUNÇÃO PARA FILTRAGEM DE DADOS NA CAIXA SELETORA DO GRÁFICO DE MODELOS DE AERONAVES
def filtro_aeromodelos(opcao, valor):
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

# FUNÇÃO PARA FILTRAGEM DE DADOS NA CAIXA SELETORA DO GRÁFICO DE ACIDENTES AÉREOS POR ESTADO
def filtro_acidentesUF(nome):
    if nome == "SP":
        y = SP
    elif nome == "RS":
        y = RS
    elif nome == "MT":
        y = MT
    elif nome == "PA":
        y = PA
    elif nome == "PR":
        y = PR
    elif nome == "MG":
        y = MG
    elif nome == "GO":
        y = GO
    elif nome == "MS":
        y = MS
    elif nome == "AM":
        y = AM
    elif nome == "BA":
        y = BA
    elif nome == "SC":
        y = SC
    elif nome == "MA":
        y = MA
    elif nome == "RR":
        y = RR
    elif nome == "RJ":
        y = RJ
    elif nome == "TO":
        y = TO
    elif nome == "PI":
        y = PI
    elif nome == "PE":
        y = PE
    elif nome == "CE":
        y = CE
    elif nome == "AC":
        y = AC
    elif nome == "ES":
        y = ES
    elif nome == "AL":
        y = AL
    elif nome == "AP":
        y = AP
    elif nome == "RO":
        y = RO
    elif nome == "SE":
        y = SE
    elif nome == "DF":
        y = DF
    elif nome == "INDEFINIDO":
        y = INDEFINIDO
    elif nome == "PB":
        y = PB
    elif nome == "RN":
        y = RN

    return y

# CHAMANDO O DECORADOR DO GRÁFICO DE MODELOS DE AERONAVES
@app.callback(
    Output("grafico-barras-aeronaves", "figure"),
    Input("dropdown-aeronaves", "value"),
    Input('RadioItems-aeronaves', 'value')
)

# Definindo os valores de x e y para o gráfico de Modelos de Aeronaves
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

# CHAMANDO O DECORADOR DO GRÁFICO DE ACIDENTES AÉREOS POR ESTADOS
@app.callback(
    Output("grafico-barras-acidentesUF", "figure"),
    Input("dropdown-acidentes", 'value')
)

# Definindo os valores de x e y para o gráfico de Acidentes Aéros por Estado
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

# Executando a aplicação no servidor local
if __name__ == '__main__':
    app.run_server(debug = True, use_reloader = False)