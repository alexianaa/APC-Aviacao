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
df_passageiros = pd.read_csv('Fluxo - Passageiros.csv', quotechar='"') 

# Criação das listas de fluxo de passageiros por empresas e atribuição de dados às listas
data = df_passageiros.values[:,0] 
gol_passageiros= df_passageiros.values[:,1]
tam_passageiros = df_passageiros.values[:,2]
azul_passageiros = df_passageiros.values[:,3]
avianca_passageiros = df_passageiros.values[:,4]
passaredo_passageiros = df_passageiros.values[:,5]

# Leitura da base de dados de fluxo de decolagens
df_decolagens = pd.read_csv('Fluxo - Decolagens.csv', quotechar='"') 

# Criação das listas de fluxo de decolagens por empresas e atribuição de dados às listas
gol_decolagens = df_decolagens.values[:,1]
tam_decolagens = df_decolagens.values[:,2]
azul_decolagens = df_decolagens.values[:,3]
avianca_decolagens = df_decolagens.values[:,4]
passaredo_decolagens = df_decolagens.values[:,5]

# Leitura da base de dados do fluxo de passageiros por decolagens
df_passageiros_por_decolagem = pd.read_csv('Fluxo - Passageiros por Decolagem.csv', quotechar='"')

#Criação das listas de fluxo de passageiros por decolagem por empresas e atribuição de dados às listas
gol_passageiros_por_decolagem = df_passageiros_por_decolagem.values[:,1]
tam_passageiros_por_decolagem = df_passageiros_por_decolagem.values[:,2]
azul_passageiros_por_decolagem = df_passageiros_por_decolagem.values[:,3]
avianca_passageiros_por_decolagem = df_passageiros_por_decolagem.values[:,4]
passaredo_passageiros_por_decolagem = df_passageiros_por_decolagem.values[:,5]


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
fig_passageiros = go.Figure()
fig_passageiros.add_trace(go.Scatter(x = data, y = gol_passageiros, mode='lines', name= 'GOL', line=dict(color="orange")))
fig_passageiros.add_trace(go.Scatter(x = data, y = tam_passageiros, mode='lines', name= 'TAM', line=dict(color="red")))
fig_passageiros.add_trace(go.Scatter(x = data, y = azul_passageiros, mode='lines', name= 'AZUL', line=dict(color="blue")))
fig_passageiros.add_trace(go.Scatter(x = data, y = avianca_passageiros, mode='lines', name= 'AVIANCA', line=dict(color="darkred")))
fig_passageiros.add_trace(go.Scatter(x = data, y = passaredo_passageiros, mode='lines', name= 'PASSAREDO', line=dict(color="yellow")))
fig_passageiros.update_layout(title='FLUXO DE PASSAGEIROS',
                     xaxis_title='Mês', 
                     yaxis_title='Número de Passageiros')

# criação do gráfico de fluxo de decolagens
fig_decolagens = go.Figure() 
fig_decolagens.add_trace(go.Scatter(x = data, y = gol_decolagens, mode='lines', name= 'GOL', line=dict(color="orange")))
fig_decolagens.add_trace(go.Scatter(x = data, y = tam_decolagens, mode='lines', name= 'TAM', line=dict(color="red")))
fig_decolagens.add_trace(go.Scatter(x = data, y = azul_decolagens, mode='lines', name= 'AZUL', line=dict(color="blue")))
fig_decolagens.add_trace(go.Scatter(x = data, y = avianca_decolagens, mode='lines', name= 'AVIANCA', line=dict(color="darkred")))
fig_decolagens.add_trace(go.Scatter(x = data, y = passaredo_decolagens, mode='lines', name= 'PASSAREDO', line=dict(color="yellow")))
fig_decolagens.update_layout(title='FLUXO DE DECOLAGENS',
                     xaxis_title='Mês', 
                     yaxis_title='Número de Decolagens')

# criação do gráfico de fluxo de passageiros por decolagens
fig_passageiros_por_decolagem = go.Figure() 
fig_passageiros_por_decolagem.add_trace(go.Scatter(x = data, y = gol_passageiros_por_decolagem, mode='lines', name= 'GOL', line=dict(color="orange")))
fig_passageiros_por_decolagem.add_trace(go.Scatter(x = data, y = tam_passageiros_por_decolagem, mode='lines', name= 'TAM', line=dict(color="red")))
fig_passageiros_por_decolagem.add_trace(go.Scatter(x = data, y = azul_passageiros_por_decolagem, mode='lines', name= 'AZUL', line=dict(color="blue")))
fig_passageiros_por_decolagem.add_trace(go.Scatter(x = data, y = avianca_passageiros_por_decolagem, mode='lines', name= 'AVIANCA', line=dict(color="darkred")))
fig_passageiros_por_decolagem.add_trace(go.Scatter(x = data, y = passaredo_passageiros_por_decolagem, mode='lines', name= 'PASSAREDO', line=dict(color="yellow")))
fig_passageiros_por_decolagem.update_layout(title='FLUXO DE PASSAGEIROS POR DECOLAGEM',
                     xaxis_title='Mês', 
                     yaxis_title='Passageiros por Decolagem')

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
    dcc.Dropdown(                               
        id="dropdown-aeronaves",               
        options=[                               
            {'label': opcao, 'value': opcao}    
            for opcao in opcoes_filtro          
        ],
        value = opcoes_filtro[0],              
        clearable=False,                        
    ),
    dcc.RadioItems(                            
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
    html.Div('Fluxo de passageiros e decolagens por empresa', style={'color': 'grey', 'fontSize': 30}),
    dcc.Graph(figure = fig_passageiros), #fluxo
    dcc.Graph(figure = fig_decolagens), #fluxo
    dcc.Graph(figure = fig_passageiros_por_decolagem), #fluxo
    
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
    if nome == "RS":
        y = RS
    if nome == "MT":
        y = MT
    if nome == "PA":
        y = PA
    if nome == "PR":
        y = PR
    if nome == "MG":
        y = MG
    if nome == "GO":
        y = GO
    if nome == "MS":
        y = MS
    if nome == "AM":
        y = AM
    if nome == "BA":
        y = BA
    if nome == "SC":
        y = SC
    if nome == "MA":
        y = MA
    if nome == "RR":
        y = RR
    if nome == "RJ":
        y = RJ
    if nome == "TO":
        y = TO
    if nome == "PI":
        y = PI
    if nome == "PE":
        y = PE
    if nome == "CE":
        y = CE
    if nome == "AC":
        y = AC
    if nome == "ES":
        y = ES
    if nome == "AL":
        y = AL
    if nome == "AP":
        y = AP
    if nome == "RO":
        y = RO
    if nome == "SE":
        y = SE
    if nome == "DF":
        y = DF
    if nome == "INDEFINIDO":
        y = INDEFINIDO
    if nome == "PB":
        y = PB
    if nome == "RN":
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

# Executando a aplicação no servidor local
if __name__ == '__main__':
    app.run_server(debug = True, use_reloader = False)