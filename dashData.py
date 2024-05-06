import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dash_table import DataTable

# Carregar os dados do CSV para um DataFrame
df = pd.read_csv('MERCADOPAGOFORMATTED.csv', sep=';', parse_dates=['DATE'])
df_summary = df[['DATE', 'DESCRIPTION', 'GROSS_AMOUNT', 'NET_CREDIT_AMOUNT', 'NET_DEBIT_AMOUNT', 'MP_FEE_AMOUNT', 'FINANCING_FEE_AMOUNT', 'SHIPPING_FEE_AMOUNT', 'TAXES_AMOUNT', 'COUPON_AMOUNT', 'PAYMENT_METHOD']]
df_grouped = df_summary.groupby('DATE').sum().reset_index()

# Iniciar o aplicativo Dash 
app = dash.Dash(__name__)

# Layout do aplicativo
app.layout = html.Div([
    html.H1("Dashboard de Transações"),

     html.Div([
    dcc.Dropdown(
        id='date-dropdown',
        options=[{'label': date, 'value': date} for date in df_grouped['DATE']],
        value=df_grouped['DATE'].min(),
        clearable=False
    ),
    html.Div(id='table-container')
]),

    html.Div(id='data-table-container'),
    dcc.Graph(
        id='graph-summary',
        figure=px.line(df_grouped, x='DATE', y=['GROSS_AMOUNT', 'MP_FEE_AMOUNT', 'FINANCING_FEE_AMOUNT', 'SHIPPING_FEE_AMOUNT', 'TAXES_AMOUNT', 'COUPON_AMOUNT'], title='Valores Totais por Data')
    ),
    dcc.Graph(
        id='pie-chart-summary',
        figure=px.pie(df_summary, names='PAYMENT_METHOD', title='Distribuição dos Métodos de Pagamento')
    ),

    html.H2("Análise da Distribuição dos Valores"),
    dcc.Graph(
        id='histogram',
        figure=px.histogram(df_summary, x='GROSS_AMOUNT', nbins=30, title='Distribuição do Valor Bruto das Transações')
    ),
    dcc.Graph(
        id='box-plot',
        figure=px.box(df_summary, y='NET_CREDIT_AMOUNT', title='Boxplot do Valor Líquido das Transações')
    ),

    html.H2("Tendência Temporal dos Valores"),
    dcc.Graph(
        id='line-chart-net',
        figure=px.line(df_grouped, x='DATE', y=['NET_CREDIT_AMOUNT', 'NET_DEBIT_AMOUNT'], title='Tendência Temporal dos Valores Líquidos')
    ),
    dcc.Graph(
        id='line-chart-gross',
        figure=px.line(df_grouped, x='DATE', y='GROSS_AMOUNT', title='Tendência Temporal do Valor Bruto')
    )
])

@app.callback(
    dash.dependencies.Output('data-table-container', 'children'),
    [dash.dependencies.Input('date-dropdown', 'value')]
)
def update_data_table(selected_date):
    data = df[df['DATE'].dt.date == pd.to_datetime(selected_date).date()]
    total_transactions = len(data)
    revenue = data['NET_CREDIT_AMOUNT'].sum()
    mpfee = data['MP_FEE_AMOUNT'].sum()
    shipfee = data['SHIPPING_FEE_AMOUNT'].sum()
    profit = revenue + mpfee + shipfee
    taxes = mpfee + shipfee

    # Filtrar entradas e saídas
    entries = data[data['NET_CREDIT_AMOUNT'] > 0]
    exits = data[data['NET_DEBIT_AMOUNT'] > 0]
    shipping_fee = data[data['SHIPPING_FEE_AMOUNT'] != 0]
    mp_fee = data[data['MP_FEE_AMOUNT'] != 0]



    entries_by_description = entries.groupby('DESCRIPTION')['NET_CREDIT_AMOUNT'].sum()
    exits_by_description = exits.groupby('DESCRIPTION')['NET_DEBIT_AMOUNT'].sum()
    mp_fee_by_description = mp_fee.groupby('DESCRIPTION')['MP_FEE_AMOUNT'].sum()
    shipping_fee_by_description = shipping_fee.groupby('DESCRIPTION')['SHIPPING_FEE_AMOUNT'].sum()

    return html.Div([
        html.H2(f"Data: {selected_date}"),
        html.P(f"Total de movimentações: {total_transactions}"),
        html.P(f"Receita Grosso: R${revenue:.2f}"),
        html.P(f"Receita líquido: R${profit:.2f}"),
        html.P(f"Total Taxas: R${taxes:.2f}"),
        html.P(f"Taxa Mercado Pago: R${mpfee:.2f}"),
        html.P(f"Taxa Frete: R${shipfee:.2f}"),
        html.H3("Movimentações realizadas no dia:"),
        html.H4("Entradas:"),
        DataTable(
            columns=[{'name': col, 'id': col} for col in ['DESCRIPTION', 'NET_CREDIT_AMOUNT']],
            data=entries_by_description.reset_index().to_dict('records'),

        ),
        html.H4("Saídas:"),
        DataTable(
            columns=[{'name': col, 'id': col} for col in ['DESCRIPTION', 'NET_DEBIT_AMOUNT']],
            data=exits_by_description.reset_index().to_dict('records')
        ),
        html.H4("Taxas Mercado Pago:"),
        DataTable(
            columns=[{'name': col, 'id': col} for col in ['DESCRIPTION', 'MP_FEE_AMOUNT']],
            data=mp_fee_by_description.reset_index().to_dict('records')
        ),
         html.H4("Taxas Frete:"),
        DataTable(
            columns=[{'name': col, 'id': col} for col in ['DESCRIPTION', 'SHIPPING_FEE_AMOUNT']],
            data=shipping_fee_by_description.reset_index().to_dict('records'),
        ),
    ])

# Executar o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)