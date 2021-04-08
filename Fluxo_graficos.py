import plotly.graph_objects as go
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash
import dash_core_components as dcc
import dash_html_components as html

df_ps = pd.read_csv('Fluxo - Passageiros.csv', quotechar='"')
data_ps = df_ps.values[:,0]
gol_ps= df_ps.values[:,1]
tam_ps = df_ps.values[:,2]
azul_ps = df_ps.values[:,3]
avianca_ps = df_ps.values[:,4]
passaredo_ps = df_ps.values[:,5]

fig_ps = go.Figure()
fig_ps.add_trace(go.Scatter(x = data_ps, y = gol_ps, mode='lines', name= 'GOL', line=dict(color="orange")))
fig_ps.add_trace(go.Scatter(x = data_ps, y = tam_ps, mode='lines', name= 'TAM', line=dict(color="red")))
fig_ps.add_trace(go.Scatter(x = data_ps, y = azul_ps, mode='lines', name= 'AZUL', line=dict(color="blue")))
fig_ps.add_trace(go.Scatter(x = data_ps, y = avianca_ps, mode='lines', name= 'AVIANCA', line=dict(color="darkred")))
fig_ps.add_trace(go.Scatter(x = data_ps, y = passaredo_ps, mode='lines', name= 'PASSAREDO', line=dict(color="yellow")))
fig_ps.update_layout(title='PASSAGEIROS',
                     xaxis_title='Mês', 
                     yaxis_title='Número de Passageiros')

df_dcl = pd.read_csv('Fluxo - Decolagens.csv', quotechar='"')
data_dcl = df_dcl.values[:,0]
gol_dcl = df_dcl.values[:,1]
tam_dcl = df_dcl.values[:,2]
azul_dcl = df_dcl.values[:,3]
avianca_dcl = df_dcl.values[:,4]
passaredo_dcl = df_dcl.values[:,5]

fig_dcl = go.Figure()
fig_dcl.add_trace(go.Scatter(x = data_dcl, y = gol_dcl, mode='lines', name= 'GOL', line=dict(color="orange")))
fig_dcl.add_trace(go.Scatter(x = data_dcl, y = tam_dcl, mode='lines', name= 'TAM', line=dict(color="red")))
fig_dcl.add_trace(go.Scatter(x = data_dcl, y = azul_dcl, mode='lines', name= 'AZUL', line=dict(color="blue")))
fig_dcl.add_trace(go.Scatter(x = data_dcl, y = avianca_dcl, mode='lines', name= 'AVIANCA', line=dict(color="darkred")))
fig_dcl.add_trace(go.Scatter(x = data_dcl, y = passaredo_dcl, mode='lines', name= 'PASSAREDO', line=dict(color="yellow")))
fig_dcl.update_layout(title='DECOLAGENS',
                     xaxis_title='Mês', 
                     yaxis_title='Número de Decolagens')

df_ppd = pd.read_csv('Fluxo - Passageiros por Decolagem.csv', quotechar='"')
data_ppd = df_ppd.values[:,0]
gol_ppd = df_ppd.values[:,1]
tam_ppd = df_ppd.values[:,2]
azul_ppd = df_ppd.values[:,3]
avianca_ppd = df_ppd.values[:,4]
passaredo_ppd = df_ppd.values[:,5]

fig_ppd = go.Figure()
fig_ppd.add_trace(go.Scatter(x = data_ppd, y = gol_ppd, mode='lines', name= 'GOL', line=dict(color="orange")))
fig_ppd.add_trace(go.Scatter(x = data_ppd, y = tam_ppd, mode='lines', name= 'TAM', line=dict(color="red")))
fig_ppd.add_trace(go.Scatter(x = data_ppd, y = azul_ppd, mode='lines', name= 'AZUL', line=dict(color="blue")))
fig_ppd.add_trace(go.Scatter(x = data_ppd, y = avianca_ppd, mode='lines', name= 'AVIANCA', line=dict(color="darkred")))
fig_ppd.add_trace(go.Scatter(x = data_ppd, y = passaredo_ppd, mode='lines', name= 'PASSAREDO', line=dict(color="yellow")))
fig_ppd.update_layout(title='PASSAGEIROS POR DECOLAGEM',
                     xaxis_title='Mês', 
                     yaxis_title='Passageiros por Decolagem')

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure = fig_ps),
    dcc.Graph(figure = fig_dcl),
    dcc.Graph(figure = fig_ppd)
])
app.run_server(debug = True)