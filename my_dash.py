import pandas as pd
import glob
import plotly.express as px
from dash import Dash, html, dcc, Output, Input, dash_table

# ---- Data Loading and Processing ----

folder_pattern = 'scrapers/data/*'
matching_folders = glob.glob(folder_pattern)

dataframes_global = []
dataframes_notebooks = []

for folder in matching_folders:
    mexx_files = glob.glob(f'{folder}/mexx-*.csv')
    venex_files = glob.glob(f'{folder}/venex-*.csv')
    notebooks_files = glob.glob(f'{folder}/*notebooks-*.csv')

    mexx_files = [file for file in mexx_files if 'notebooks' not in file]
    venex_files = [file for file in venex_files if 'notebooks' not in file]

    for file in mexx_files + venex_files:
        df = pd.read_csv(file)
        dataframes_global.append(df)

    for file in notebooks_files:
        df_notebooks = pd.read_csv(file)
        dataframes_notebooks.append(df_notebooks)

combined_data_global_all = pd.concat(dataframes_global, ignore_index=True)


combined_data_notebooks_all = pd.concat(dataframes_notebooks, ignore_index=True)
#elimino registros repetidos
combined_data_global = combined_data_global_all.drop_duplicates(
    subset=combined_data_global_all.columns.difference(['created_at'])
)
combined_data_notebooks = combined_data_notebooks_all.drop_duplicates(
    subset=combined_data_notebooks_all.columns.difference(['created_at'])
)

category_percentage_mexx = combined_data_global[combined_data_global['store'] == 'mexx']['category'].value_counts(normalize=True) * 100
category_percentage_mexx = category_percentage_mexx.reset_index()
category_percentage_mexx.columns = ['category', 'percentage']
category_percentage_mexx['store'] = 'mexx'

category_percentage_venex = combined_data_global[combined_data_global['store'] == 'venex']['category'].value_counts(normalize=True) * 100
category_percentage_venex = category_percentage_venex.reset_index()
category_percentage_venex.columns = ['category', 'percentage']
category_percentage_venex['store'] = 'venex'

combined_df = pd.concat([category_percentage_mexx, category_percentage_venex])

fig_combined = px.bar(
    combined_df,
    x='category',
    y='percentage',
    color='store',
    title='Porcentaje de productos obtenidos por Categoría',
    labels={'category': 'Categoría', 'percentage': 'Porcentaje (%)'},
    barmode='group'
)

combined_data_notebooks['brand'] = combined_data_notebooks['brand'].apply(str.rstrip)
brand_avg_price = combined_data_notebooks.groupby('brand')['cash_price'].mean().reset_index()
fig_brand = px.bar(brand_avg_price, x='brand', y='cash_price', title='Comparación de Precios por Marca')

avg_price_by_category_store = combined_data_global.groupby(['category', 'store'])['cash_price'].mean().reset_index()
fig_price_comparison = px.bar(avg_price_by_category_store, 
                              x='category', 
                              y='cash_price', 
                              color='store', 
                              title='Comparación de Precio Promedio por Categoría entre Tiendas', 
                              barmode='group',
                              labels={'cash_price': 'Precio Promedio ($)', 'category': 'Categoría'})

brand_options = [{'label': brand, 'value': brand} for brand in combined_data_notebooks['brand'].unique()]
processor_options = [{'label': processor, 'value': processor} for processor in combined_data_notebooks['processor'].unique()]

# ---- Dash App ----

app = Dash(__name__)

combined_df_table = dash_table.DataTable(
    data=combined_data_global.to_dict('records'),
    columns=[{'name': col, 'id': col} for col in combined_data_global.columns],
    style_table={'maxHeight': '400px', 'overflowY': 'scroll'},
)

notebooks_table = dash_table.DataTable(
    data=combined_data_notebooks.to_dict('records'),
    columns=[{'name': col, 'id': col} for col in combined_data_notebooks.columns],
    style_table={'maxHeight': '400px', 'overflowY': 'scroll'},
)

app.layout = html.Div([
    html.H1("Visualización de Datos"),
    dcc.Tabs([
        dcc.Tab(label='Comparación de Stores', children=[
            html.H1(children='Hardware Pricing', style={'textAlign':'center'}),
            combined_df_table,
            dcc.Graph(id='category-percentage-combined', figure=fig_combined),
            dcc.Graph(id='category-store-price-comparison', figure=fig_price_comparison),
        ]),
        dcc.Tab(label='Comparación de Notebooks', children=[
            html.H1(children='Notebook Comparación', style={'textAlign':'center'}),
            notebooks_table,
            dcc.Graph(id='brand-price-comparison', figure=fig_brand),
            dcc.Dropdown(id='brand-dropdown', options=brand_options, multi=True, placeholder="Selecciona Marca(s)"),
            dcc.Dropdown(id='processor-dropdown', options=processor_options, multi=True, placeholder="Selecciona Procesador(es)"),
            dcc.Graph(id='notebook-histogram'),
        ]),
    ]),
])

@app.callback(
    Output('notebook-histogram', 'figure'),
    [Input('brand-dropdown', 'value'),
     Input('processor-dropdown', 'value')]
)
def update_histogram(selected_brands, selected_processors):
    filtered_data = combined_data_notebooks.copy()
    if selected_brands:
        filtered_data = filtered_data[filtered_data['brand'].isin(selected_brands)]
    if selected_processors:
        filtered_data = filtered_data[filtered_data['processor'].isin(selected_processors)]
    histogram_fig = px.histogram(filtered_data, x='cash_price', nbins=10, title='Histograma de Precios de Notebooks')
    return histogram_fig

if __name__ == '__main__':
    app.run_server(debug=True)
