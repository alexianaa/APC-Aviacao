import plotly.graph_objects as go
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash
import dash_core_components as dcc
import dash_html_components as html

df_passageiros = pd.read_csv('Fluxo - Passageiros.csv', quotechar='"') #faz referência ao csv de número de passageiros
data = df_passageiros.values[:,0] #define a data que sera utilizada no eixo x em todos os gráficos
#define os valores de passageiros, será utilizado no eixo y de seu respectivo gráfico
gol_passageiros= df_passageiros.values[:,1]
tam_passageiros = df_passageiros.values[:,2]
azul_passageiros = df_passageiros.values[:,3]
avianca_passageiros = df_passageiros.values[:,4]
passaredo_passageiros = df_passageiros.values[:,5]

#criação do gráfico
fig_passageiros = go.Figure() #nome do gráfico
#valores do gráfico
fig_passageiros.add_trace(go.Scatter(x = data, y = gol_passageiros, mode='lines', name= 'GOL', line=dict(color="orange")))
fig_passageiros.add_trace(go.Scatter(x = data, y = tam_passageiros, mode='lines', name= 'TAM', line=dict(color="red")))
fig_passageiros.add_trace(go.Scatter(x = data, y = azul_passageiros, mode='lines', name= 'AZUL', line=dict(color="blue")))
fig_passageiros.add_trace(go.Scatter(x = data, y = avianca_passageiros, mode='lines', name= 'AVIANCA', line=dict(color="darkred")))
fig_passageiros.add_trace(go.Scatter(x = data, y = passaredo_passageiros, mode='lines', name= 'PASSAREDO', line=dict(color="yellow")))
fig_passageiros.update_layout(title='PASSAGEIROS',
                     xaxis_title='Mês', 
                     yaxis_title='Número de Passageiros')

df_decolagens = pd.read_csv('Fluxo - Decolagens.csv', quotechar='"') #faz referência ao csv de número de decolagens
#define os valores de decolagens, será utilizado no eixo y de seu respectivo gráfico
gol_decolagens = df_decolagens.values[:,1]
tam_decolagens = df_decolagens.values[:,2]
azul_decolagens = df_decolagens.values[:,3]
avianca_decolagens = df_decolagens.values[:,4]
passaredo_decolagens = df_decolagens.values[:,5]

#criação do gráfico
fig_decolagens = go.Figure() #nome do gráfico
#valores do gráfico
fig_decolagens.add_trace(go.Scatter(x = data, y = gol_decolagens, mode='lines', name= 'GOL', line=dict(color="orange")))
fig_decolagens.add_trace(go.Scatter(x = data, y = tam_decolagens, mode='lines', name= 'TAM', line=dict(color="red")))
fig_decolagens.add_trace(go.Scatter(x = data, y = azul_decolagens, mode='lines', name= 'AZUL', line=dict(color="blue")))
fig_decolagens.add_trace(go.Scatter(x = data, y = avianca_decolagens, mode='lines', name= 'AVIANCA', line=dict(color="darkred")))
fig_decolagens.add_trace(go.Scatter(x = data, y = passaredo_decolagens, mode='lines', name= 'PASSAREDO', line=dict(color="yellow")))
fig_decolagens.update_layout(title='DECOLAGENS',
                     xaxis_title='Mês', 
                     yaxis_title='Número de Decolagens')

df_passageiros_por_decolagem = pd.read_csv('Fluxo - Passageiros por Decolagem.csv', quotechar='"') #faz referência ao csv de número de passageiros por decolagem
#define os valores de decolagens, será utilizado no eixo y de seu respectivo gráfico
gol_passageiros_por_decolagem = df_passageiros_por_decolagem.values[:,1]
tam_passageiros_por_decolagem = df_passageiros_por_decolagem.values[:,2]
azul_passageiros_por_decolagem = df_passageiros_por_decolagem.values[:,3]
avianca_passageiros_por_decolagem = df_passageiros_por_decolagem.values[:,4]
passaredo_passageiros_por_decolagem = df_passageiros_por_decolagem.values[:,5]

#criação do gráfico
fig_passageiros_por_decolagem = go.Figure() #nome do gráfico
#valores do gráfico
fig_passageiros_por_decolagem.add_trace(go.Scatter(x = data, y = gol_passageiros_por_decolagem, mode='lines', name= 'GOL', line=dict(color="orange")))
fig_passageiros_por_decolagem.add_trace(go.Scatter(x = data, y = tam_passageiros_por_decolagem, mode='lines', name= 'TAM', line=dict(color="red")))
fig_passageiros_por_decolagem.add_trace(go.Scatter(x = data, y = azul_passageiros_por_decolagem, mode='lines', name= 'AZUL', line=dict(color="blue")))
fig_passageiros_por_decolagem.add_trace(go.Scatter(x = data, y = avianca_passageiros_por_decolagem, mode='lines', name= 'AVIANCA', line=dict(color="darkred")))
fig_passageiros_por_decolagem.add_trace(go.Scatter(x = data, y = passaredo_passageiros_por_decolagem, mode='lines', name= 'PASSAREDO', line=dict(color="yellow")))
fig_passageiros_por_decolagem.update_layout(title='PASSAGEIROS POR DECOLAGEM',
                     xaxis_title='Mês', 
                     yaxis_title='Passageiros por Decolagem')

#apresentação do gráfico no dash
app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure = fig_passageiros),
    dcc.Graph(figure = fig_decolagens),
    dcc.Graph(figure = fig_passageiros_por_decolagem)
])
app.run_server(debug = True)