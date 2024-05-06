import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html

# Carregar os dados do CSV para um DataFrame
df = pd.read_csv('MERCADOPAGO.csv', sep=';', parse_dates=['DATE'])

# Selecionar os dados relevantes
df_summary = df[['DATE', 'DESCRIPTION', 'GROSS_AMOUNT', 'NET_CREDIT_AMOUNT', 'NET_DEBIT_AMOUNT', 'MP_FEE_AMOUNT', 'FINANCING_FEE_AMOUNT', 'SHIPPING_FEE_AMOUNT', 'TAXES_AMOUNT', 'COUPON_AMOUNT', 'PAYMENT_METHOD']]

# Agrupar os dados por data
df_grouped = df.groupby('DATE').sum().reset_index()

# Iniciar o aplicativo Dash
app = dash.Dash(__name__)

# Layout do aplicativo
app.layout = html.Div([
    html.H1("Dashboard de Transações"),
    
    html.H2("Resumo dos Valores Totais"),
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

# Executar o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)
