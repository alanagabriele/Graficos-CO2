from pandas import read_csv
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

app = Dash(__name__, title='Emissão de CO2')

df = read_csv("annual-co2-emissions-per-country.csv")

df_array = df.values #Tranformando tudo o que estiver no df em uma lista para parar de usar a extensão Pandas no código.

#---------------------------------------------------------------------------------------------------------
#Grafico1

world = []
anos = []

# Colocando os dados do mundo na lista vazia
for linha in df_array:
    anos.append(linha[2])
    if linha[0] == "World":
        world.append(linha[3])

anos = sorted(set(anos))

fig1 = px.line(
    x=anos,
    y=world,
    color_discrete_sequence=px.colors.sequential.Aggrnyl,
    template='gridon',
    title="Emissão no mundo ao longo do tempo",
    labels={
        "y":"Emissão ",
        "x":"Ano "
    }
)

fig1.update_layout(
    title="Emissão no mundo ao longo do tempo",
    xaxis_title="Anos",
    yaxis_title="Emissão por tonelada",
    paper_bgcolor="rgba(255,255,255,0)",
    plot_bgcolor="#DCEEF3",
    title_font_family="Archive",
    title_font_color="#031225",
    font_color="#031225",
    font_family="Archive"
    )

#---------------------------------------------------------------------------------------------------------
#Grafico2

anos_ordenados = []
paises_ordenados = []
nivel_ordenado = []
codigo_ordenado = []

for ano in anos:
    for linha in df_array:
        if linha[2] == ano:
            if (linha[0] != 'Africa') and (linha[0] != 'Asia') and (linha[0] != 'Europe') and (linha[0] != 'North America') and (linha[0] != 'Oceania') and (linha[0] != 'South America') and (linha[0] != 'World'):
                paises_ordenados.append(linha[0])
                codigo_ordenado.append(linha[1])
                anos_ordenados.append(linha[2])
                nivel_ordenado.append(linha[3])

fig2 = px.choropleth(
    locations=codigo_ordenado, #Posição do país no mapa
    color=nivel_ordenado, #Nível de CO2
    hover_name=paises_ordenados, #Nome do país ao deixar o mouse encima
    animation_frame=anos_ordenados, #Régua
    range_color=[0,2000000000], #Intervalo de CO2
    color_continuous_scale=px.colors.sequential.Mint, #Variação de cor
    labels={
        "animation_frame":"Ano ",
        "color":"Emissão ",
        "locations":"Código "
    }
)

fig2.update_layout(
    title_font_family="Archive",
    title_font_color="#031225",
    font_color="#031225",
    font_family="Archive",
    paper_bgcolor="#DCEEF3"
)

#---------------------------------------------------------------------------------------------------------
#Dados para Gráficos 3 e 4.

# Dicionário com os continentes
emissoes =	{
  'Africa': [], # Continentes/Key : valor(es) = (lista vazia)
  'Asia': [],
  'Europe': [],
  'North America': [],
  'Oceania': [],
  'South America': [],
}

anos = []

# Adicionando os dados de emissão para cada lista de continentes do dicionário
for linha in df_array:
    if linha[2] >= 1987:
        anos.append(linha[2])

    anos = sorted(set(anos))
    for ano in anos:
        for emissao in emissoes:
            if linha[0] == emissao: # continente sendo lido no momento no df == 'key' do dicionário.
                if linha[2] == ano: # Não queremos todos os anos, filtramos ele.
                    emissoes[emissao].append(linha[3])


continents = ['Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America'] #Original do CSV
continentes = ['África', 'Ásia', 'Europa', 'América do Norte', 'Oceania', 'América do Sul'] # Traduzido

#----------------------------
#Grafico3

fig3 = px.bar(
    x=anos, 
    y=anos)

#----------------------------
#Grafico4

fig4 = px.pie(
  names= continentes,
  values= continentes)

#---------------------------------------------------------------------------------------------------------
#HTML - Esqueleto da página Dash
app.layout = html.Main(id='graphs', className='container',
    children = [
        html.Div(className="menu",
            children= [
                html.Img(id='logo',
                    src='assets\Logo.jpg'),
                html.Div(className="ancoras",
                    children=[ 
                        html.A(className="line", children=[
                            html.Img(src='./assets/grafico-de-linha.png', id='linhaPng'),
                            html.Img(src='./assets/grafico-de-linha.gif', id='linhaGif')
                        ],
                            href="#grafic1"),
                        html.A(className="map", children=[
                            html.Img(src='./assets/grafico-mapa.png', id='mapaPng'),
                            html.Img(src='./assets/grafico-mapa.gif', id='mapaGif')
                        ], href="#grafico_mapa_CO2"),
                        html.A(className="bar", children=[
                            html.Img(src='./assets/grafico-de-barras.png', id='barraPng'),
                            html.Img(src='./assets/grafico-de-barras.gif', id='barraGif')
                        ], href="#grafico_Barras_CO2"),
                        html.A(className="pie", children=[
                            html.Img(src='./assets/grafico-de-pizza.png', id='pizzaPng'),
                            html.Img(src='./assets/grafico-de-pizza.gif', id='pizzaGif')
                        ], href="#grafico_Pizza_CO2")
                    ]
                )
            ]
        ),
        html.Div(className='graficos',
            children=[
                html.Div(className='capa',
                children=[
                    html.H1(id='texto1',
                        children=[
                            "Emissão", html.Br(), "global de", html.Br(), "CO2"
                        ]
                    ),
                    html.Img(src='assets\mundo.png', id='mundo'),
                    html.Div(id='grafic1')
                ]),
                html.Div(className='grafico_1',
                    children = [
                        html.Div(className='T1', children=[
                            html.H1('Gráfico de Linha', id="T_Grafico1"),
                            html.H2(
                                children=[
                                    html.P('Como as emissões de CO2 mudaram ao longo do tempo?'), html.P('Pode-se notar o crescimento global da emissão por tonelada de CO2 em relação ao tempo, tendo início em 1750 e possuindo dados até 2020.'), html.P('Por meio deste gráfico, é possível observar uma emissão quase nula nos primeiros cem anos, seguida de uma alta a partir do século XX, momento no qual a humanidade começou processos maiores de industrialização.'), html.P('Ao final do século XX, já havia atingido 22 bilhões de toneladas, com o gráfico ainda tendendo a crescer.'), html.P('Nos últimos anos, a emissão de CO2 está próxima das 35 bilhões de toneladas. Vê-se que o crescimento se estabilizou no final do gráfico, porém ainda não atingiu o nível máximo.')
                                ], id='T1'
                            )
                            ]
                        ),
                        html.Div(className='g1',
                            children=[
                                dcc.Graph(id='Grafico_Linhas_CO2',
                                    figure=fig1)
                            ]
                        ),
                        html.Div(id='grafico_mapa_CO2')
                    ]
                ),
                html.Div(className='grafico_2',
                    children = [
                        html.Div(className='T2', children=[
                            html.H1('Gráfico de Mapa', id="T_Grafico2"),
                            html.H2(
                                children=[
                                    html.P('A relação da emissão de CO2 em cada país do mundo de acordo com o tempo é o foco deste gráfico.'), html.P('Países que emitem em maior escala costumam ser produtores de petróleo e gás natural ou serem ocupados por uma grande população. Há também um fator de desenvolvimento, visto que países menos desenvolvidos se apresentam com emissões muito baixas em comparação com grandes potências mundiais.'), html.P('Utilizando o recurso do gráfico para comparar datas, em 1750 o Reino Unido era o maior emissor, enquanto atualmente o norte da América e a Ásia assumem o topo das emissões.')
                                ], id='T2'
                            )
                        ]
                        ),
                        html.Div(className='g2',
                            children=[
                                dcc.Graph(id="Grafico-Mapa", figure=fig2)         
                            ]
                        ),
                        html.Div(id='grafico_Barras_CO2')
                    ]
                ),
                html.Div(className='grafico_3',
                    children = [
                        html.Div(className='T3', children=[
                            html.H1('Gráfico de Barras', id="T_Grafico3"),
                            html.H2(
                                children=[
                                    html.P('São apresentados os dados de emissão de CO2 ao longo do tempo, especificados por cada continente, sendo apresentada a África primeiramente.'), html.P('É evidente o crescimento das emissões em todos os continentes. Tendo como partida o ano de 1987, as emissões desde o começo do gráfico já se apresentam altas, e em alguns continentes houve uma pequena queda entre os anos de 2019 e 2020.')
                                ], id='T3'
                            )
                            ]
                        ),
                        html.Div(className='g3',
                            children=[
                                dcc.Dropdown(continents, value='Africa' , id='continentes', style={
                                    'border-radius':'10px'
                                }),
                                dcc.Graph(
                                    id='Grafico_Barras_CO2',
                                    figure=fig3
                                )
                            ]
                        ),
                        html.Div(id='grafico_Pizza_CO2')
                    ]
                ),
                html.Div(id="grafico4",className='grafico_4',
                    children = [
                        html.Div(className='T4',
                            children=[
                                html.H1('Gráfico de Pizza', id="T_Grafico4"),
                                html.H2(
                                    children=[
                                        html.P('Este gráfico apresenta os dados da emissão de CO2 por continentes em relação ao tempo, tendo início em 1987, ano no qual a Europa liderava as emissões no mundo, enquanto no ano final, 2020, o continente a liderar é a Ásia, sendo responsável por mais de um quarto da emissão global.'), html.P('A Ásia, entretanto, possui uma população altíssima, e balanceando sua emissão em relação a população, possui números baixos quando comparada com outros continentes.'), html.P('A América do Sul e a África apresentam um percentual pequeno, ambos têm emissão correspondente a voos e envio de mercadoria, mas esses dados não são considerados globalmente.')
                                    ], id='T4'
                                )
                            ]
                        ),
                        html.Div(className='g1',
                            children=[
                                dcc.Dropdown(anos, value=1987, id='Anos', style={
                                    'border-radius':'10px'
                                }),
                                dcc.Graph(
                                    id='Grafico_Pizza_CO2',
                                    figure=fig4
                                )
                            ]
                        )
                    ]
                ),
                html.Div(className='baseboard',
                    children=[
                        html.Div(className='participantes',
                            children=[
                                html.H1('Participantes - Grupo 02', id='participantes'),
                                html.H2(id='conteudo_participantes',
                                    children=[
                                        ('Alana Gabriele Amorim Silva - 211061331'), html.Br(),
                                        ('Danielle Rodrigues Silva - 211061574'), html.Br(),
                                        ('Dara Cristina Fernandes - 211061609'), html.Br(),
                                        ('Davi Rodrigues da Rocha - 211061618'), html.Br(),
                                        ('Harleny Angéllica Araújo - 211061832'), html.Br(),
                                        ('Helena Emery Silvano - 211061841'), html.Br(),
                                        ('Leandro Almeida Rocha - 211062080'), html.Br(),
                                        ('Rafaela de Melo Lopes - 211062400'), html.Br(),
                                        ('Thaiza R da Silva - 211062508')
                                    ]
                                )
                            ]
                        ),
                        html.Div(className='fonte',
                            children=[
                                html.H1('Dados Usados', id='referencia'),
                                html.H2(children=[
                                    ('Dados fornecidos pela '), html.A('Our World in Data', href='https://ourworldindata.org/co2-emissions', id='link'), (' sobre a emissão anual de CO2 por país.')], id='fonte')
                            ]
                        ),
                        html.Div(className='imagens',
                            children=[
                                html.Img(src='./assets/logo-unb.png', id='unb'),
                                html.Img(src='./assets/logo-fga.png', id='fga')
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)        

#-------------------------------------------------------------------------------------------------------------------
#Callback's

# Callback do gráfico de barras (intermediário entre a função o dropdown)
@app.callback(
    # ↓↓↓ Saída será a nova uma nova figura/gráfico com a filtragem do continente escolhido
    Output('Grafico_Barras_CO2', 'figure'),
    Input('continentes', 'value') # Entrada será o value do ID "continentes", ou seja, o dcc.dropdown.
)

# Função o G.Barras para processar o novo gráfico filtrado
def atualizar_output(value): #Definindo uma função com o parâmetro value do input recebido de callback

    for emissao in emissoes:
            if value == emissao:
                fig3 = px.bar(
                    x = anos,
                    y = emissoes[emissao],
                    color_discrete_sequence=px.colors.sequential.Aggrnyl,
                    title = 'Emissão por continente',
                    template='gridon',
                    labels={
                        "x":"Ano ",
                        "y":"Emissão ",
                    }
                )

    fig3.update_layout(
    title="Emissão por continente",
    xaxis_title="Anos",
    yaxis_title="Emissão por tonelada",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#DCEEF3",
    title_font_family="Archive",
    title_font_color="#031225",
    font_color="#031225",
    font_family="Archive"
    )

    return fig3

# Callback do Gráfico de Pizza (intermediário entre a função o dropdown)
@app.callback(
    Output('Grafico_Pizza_CO2', 'figure'),
    Input('Anos', 'value')
)

# Função o G.Pizza para processar o novo gráfico filtrado
def update_output(value):
    ano_especifico = []

    i = 0 
    while i < 34: # 33 anos entre 1987 à 2020
        if value == anos[i]:
            posição = i # Marca a posição do ano que o usuário escolheu
            break # Quebra do looping
        i += 1 # i = i + 1

    for continente in emissoes:
      # ↓↓↓ Acrescentando somente os dados de emissão, de cada continente, no índice/posição do ano específico
      ano_especifico.append(emissoes[continente][posição])

    fig4 = px.pie(
        names= continentes,
        values= ano_especifico,
        template= 'simple_white',
        title= "Emissão por continente",
        color_discrete_sequence=px.colors.sequential.Darkmint,
        labels={
            "names":"Continente ",
            "values":"Emissão "
        }
    )

    fig4.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title_font_family="Archive",
        title_font_color="#031225",
        font_color="#031225",
        font_family="Archive",
    )

    return fig4
  
#---------------------------------------------------------------------------------------------------------

# Colocando a 'app' pra rodar no Dash
if __name__ == '__main__':
    app.run_server(debug=True)