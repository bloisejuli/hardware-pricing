from dash import Dash, html,dash_table, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import glob

df_global = pd.read_csv('../data/datos_combinados.csv')
#../data/datos_combinados.csv

# Obtener una lista de nombres de archivos que coinciden con el patrón
file_pattern = '../data/*notebooks-*.csv'
matching_files = glob.glob(file_pattern)

# Crear una lista para almacenar los DataFrames individuales
dataframes = []

# Iterar sobre los nombres de archivos y cargar los datos en DataFrames individuales
for file in matching_files:
    df_notebooks = pd.read_csv(file)
    dataframes.append(df_notebooks)

combined_data = pd.concat(dataframes)
print(len(dataframes))

app = Dash(__name__)

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Pestaña 1', children=[
            html.H1(children='Hardware Pricing', style={'textAlign':'center'}),
            #tabla de datos
            dash_table.DataTable(data=df_global.to_dict('records'),page_size=10),
            # Gráfico de pastel para contar categorías
            dcc.Graph(id='pie-chart',
                    figure=px.pie(df_global, names='category', title='Category Distribution')),
            # Gráfico de barras para precios promedio por categoría
            dcc.Graph(figure=px.bar(df_global, x='category', y='cash_price', title='Average Cash Price by Category')),
            
        ]),
        dcc.Tab(label='Pestaña 2', children=[
            #tabla de datos
            dash_table.DataTable(data=combined_data.to_dict('records'),page_size=10),
            # Gráfico de barras para comparar precios para el producto seleccionado
            dcc.Graph(id='price-comparison-chart'),
            
        ])
    ])
])
@app.callback(
    Output('price-comparison-chart', 'figure'),
    [Input('price-comparison-chart', 'value')],
)


def update_graph(selected_value):
    # Agrupar y calcular el precio promedio por marca
    grouped_data = combined_data.groupby('brand').agg({
        'cash_price': 'mean',
        'memory': 'first',   # Tomamos el valor de la primera fila, ya que debería ser el mismo para la misma marca
        'storage': 'first',  # Tomamos el valor de la primera fila, ya que debería ser el mismo para la misma marca
        'processor': 'first' # Tomamos el valor de la primera fila, ya que debería ser el mismo para la misma marca
    }).reset_index()
    
    # Crear un gráfico de barras comparando los precios promedio por marca
    fig = px.bar(grouped_data, x='brand', y='cash_price', text='cash_price',
                 hover_data=['memory', 'storage', 'processor'],
                 title='Comparación de precios promedio por marca')
    
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside') # Formato para el texto en las barras
    
    return fig


if __name__ == '__main__':
    app.run(debug=True)
