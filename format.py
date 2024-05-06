import pandas as pd

# Ler o arquivo CSV
df = pd.read_csv('MERCADOPAGO.csv', sep=';')

# Converter a coluna de data para o formato desejado
df['DATE'] = pd.to_datetime(df['DATE']).dt.strftime('%Y-%m-%d')

# Salvar o arquivo CSV modificado
df.to_csv('MERCADOPAGOFORMATTED.csv', sep=';', index=False)
