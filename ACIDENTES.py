import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

tes = pd.read_excel(r"estados.xlsx") #pega a planilha do execel
dados = tes.values                   #transforma a planilha em uma lista
ano = dados[:,0]                     #variáveis que selecionam a lista e escolhe uma coluna
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

#variável que define os nomes que vai ser usado na caixa seletora
opcoes = ["SP", "RS", "MT", "PA", "PR", "MG", "GO", "MS", "AM", "BA", "SC", "MA", "RR", "RJ","TO", "PI", "PE", "CE", "AC", "ES", "AL", "AP", "RO", "SE", "DF", "INDEFINIDO", "PB", "RN"]

#variáveis que definem o nomes e os valores que serão usados no filtro
nomes_maior_menor_50 = ["Maior que 50%", "Menor que 50%", "Total"]
valor_de_maior_menor_50 = [">50", "<50", "total"]



tes = pd.read_excel(r"outros.xlsx")  #pega a planilha do execel
dados = tes.values                   #transforma a planilha em uma lista
categoria_1 = dados[:,0]             #variáveis que selecionam a lista e escolhe uma coluna
valor_1 = dados[:,1]
categoria_2 = dados[:,2]
valor_2 = dados[:,3]

#criação dos gráficos de pizza
fig_1 = go.Figure()
fig_1.add_trace(go.Pie(values = valor_1, labels = categoria_1))
fig_1.update_layout(title='ACIDENTES')

fig_2 = go.Figure()
fig_2.add_trace(go.Pie(values = valor_2, labels = categoria_2))
fig_2.update_layout(title='INCIDENTES GRAVES')


#aqui vai ser definido as configurações do grafico de barra, caixa seletora e filtro
app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Dropdown( 
        id = "filtro",                                                 #caixa seletora
        options = [{'label': nome, 'value':nome} for nome in opcoes],  #os nomes da caixa seletora será tirado da variável opcoes
        value = "SP",                                                  #nome da primeira opção
        clearable = False
    ),
    dcc.RadioItems( 
        id = "filtro_2",                                                                                                  #filtro
        options = [{'label': nome, 'value':valor} for nome, valor in zip(nomes_maior_menor_50, valor_de_maior_menor_50)], #as opções de nomes e valores tirados das variáveis nomes_maior_menor_50 e valor_de_maior_menor_50
        value = "total",                                                                                                  #primeiro valor
    ),
    dcc.Graph(id = "grafico"),  #execução dos três gráficos
    dcc.Graph(figure = fig_1),
    dcc.Graph(figure = fig_2)
])

#aqui será programado as condições para a mudança de dados (através da caixa seletora e filtro)
def separa_dados(nome, valor):    
    porcentagens_filtradas = []     #mudanças para o filtro - relativo ao eixo x
    meses_filtrados = []            #mudanças para o filtro - relativo ao eixo y
    if nome == "SP":                #mudanças do eixo y de acordo com o nome selecionado na caixa seletora
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


    if valor == ">50":                                           #no filtro, quando selecionar >50
        for porcentagem, data in zip(y, ano):                    #porcentagem = y e data = ano
            if porcentagem >= 50:                                #para y >= 50 ...
                porcentagens_filtradas.append(porcentagem)       #mostrar os selecionados
                meses_filtrados.append(data)
    elif valor == "<50":
        for porcentagem, data in zip(y, ano):
            if porcentagem <= 50:
                porcentagens_filtradas.append(porcentagem)
                meses_filtrados.append(data)
    elif valor == "total":                                        #se for "total", mostrar todos os dados
        porcentagens_filtradas = y
        meses_filtrados = ano
    return [porcentagens_filtradas, meses_filtrados]              #repati os comandos

@app.callback(
    Output(component_id='grafico', component_property= 'figure'),  #exibir gráficos e figuras
    Input(component_id='filtro', component_property='value'),      #recebe comandos para a mudança da caixa seletora
    Input(component_id='filtro_2', component_property='value')     #recebe comandos para a mudança do filtro
)


#definição do gráfico de acordo com so comandos
def grafico_1(argumento, maior_menor): 
    dados_filtrados = separa_dados(argumento, maior_menor) 
    eixo_x = dados_filtrados[1]
    eixo_y = dados_filtrados[0]
    
    linha1 = go.Bar( 
        x = eixo_x,
        y = eixo_y,
       
    )

    grafico = go.Figure(linha1)                    #criação do gráfico de barras
    grafico.update_layout(                         #estética do gráfico
        title = dict( 
            text = "Acidentes Estado x anos", 
            font = dict( 
                family = "Arial",
                size = 45,
                color = "blue"),
            xref = "paper", 
            yref = "container", 
            x = 0.5, 
            y = 0.9 
        ),
        paper_bgcolor = "black", 
        plot_bgcolor = "snow", 
    )
    return grafico                                 #repetição dos comandos para o gráfico de barras


if __name__ == '__main__':
    app.run_server(debug = True, use_reloader = False)
