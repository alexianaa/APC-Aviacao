import csv
import plotly.graph_objects as go
import pandas as pd

# Leitura da base de dados de acidentes aéreos
tes = pd.read_excel(r"estados.xlsx")
dados = tes.values

# Criação de listas das Unidades Federativas e atribuição de dados às listas 
ano = dados[:,0]
sao_paulo = dados[:,1]
rio_grande_s = dados[:,2]
mato_grosso = dados[:,3]
para = dados[:,4]
parana = dados[:,5]
minas_gerais = dados[:,6]
goias = dados[:,7]
mato_grosso_s = dados[:,8]
amazonas = dados[:,9]
bahia = dados[:,10]
santa_catarina = dados[:,11]
maranhao = dados[:,12]
roraima = dados[:,13]
rio_de_janeiro = dados[:,14]
tocantins = dados[:,15]
piaui = dados[:,16]
pernambuco = dados[:,17]
ceara = dados[:,18]
acre = dados[:,19]
espirito_santo = dados[:,20]
alagoas = dados[:,21]
amapa = dados[:,22]
rondonia = dados[:,23]
sergipe = dados[:,24]
distrito_federal = dados[:,25]
indefinido = dados[:,26]
paraiba = dados[:,27]
rio_grande_n = dados[:,28]

estados = [sao_paulo, rio_grande_s, mato_grosso, para, parana, minas_gerais, goias, mato_grosso_s, amazonas, bahia, santa_catarina, maranhao, roraima, rio_de_janeiro,  tocantins, piaui, pernambuco, ceara, acre, espirito_santo, alagoas, amapa, rondonia, sergipe, distrito_federal, indefinido, paraiba, rio_grande_n]

opcoes = ["SP", "RS", "MT", "PA", "PR", "MG", "GO", "MS", "AM", "BA", "SC", "MA", "RR", "RJ","TO", "PI", "PE", "CE", "AC", "ES", "AL", "AP", "RO", "SE", "DF", "INDEFINIDO", "PB", "RN"]

def filtro_acidentesUF(nome):
    for a,b in zip(estados,opcoes):
        if(nome == b):
            y = a
    return y

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