# Importando as bibliotecas necessárias
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# Carregar os dados do CSV
spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")

# Inicializar o aplicativo Dash
app = dash.Dash(__name__)

# Layout do dashboard
app.layout = html.Div([
    html.H1("SpaceX Launch Records Dashboard", style={'textAlign': 'center'}),
    
    # Dropdown para seleção do local de lançamento
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            *[{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()]
        ],
        value='ALL',
        placeholder="Select a Launch Site",
        searchable=True
    ),
    
    # Gráfico de pizza
    html.Div(dcc.Graph(id='success-pie-chart')),
    
    # Slider de intervalo para selecionar payload
    dcc.RangeSlider(
        id='payload-slider',
        min=0, max=10000, step=1000,
        marks={i: f'{i}' for i in range(0, 10001, 1000)},
        value=[0, 10000]
    ),
    
    # Gráfico de dispersão
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# Callback para atualizar o gráfico de pizza
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site',
                     title='Total Success Launches for All Sites')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(filtered_df, names='class',
                     title=f'Total Success vs Failed Launches for {selected_site}')
    return fig

# Callback para atualizar o gráfico de dispersão
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    low, high = payload_range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]
    if selected_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title='Payload vs. Outcome for All Sites')
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title=f'Payload vs. Outcome for {selected_site}')
    return fig

# Rodar o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)
