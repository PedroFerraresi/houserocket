import pandas as pd
from numpy import int64

data = pd.read_csv('datasets/kc_house_data.csv')

print(data.head())

# Mostra os tipos de variáveis em cada coluna
print(data.dtypes)

# Função que converte de object (String) para date
data['date'] = pd.to_datetime(data['date'])

print(data.head())
print(data.dtypes)

# ==========================================
# Conversões de Variáveis
# ==========================================

# Inteiro -> Float
data['bedrooms'] = data['bedrooms'].astype( float )
print(data.head(2))
print(data.dtypes)

# Float -> Inteiro
data['bedrooms'] = data['bedrooms'].astype( int64 )
# Muito importante sempre deixar todos os inteiros como
# int64, pois garantimos que toda e qualquer tipo de
# manipulação ou comparação seja feita corretamente.
print(data.head(2))
print(data.dtypes)

# Inteiro -> String
data['bedrooms'] = data['bedrooms'].astype( str )
print(data.head(2))
print(data.dtypes)

# String -> Inteiro
data['bedrooms'] = data['bedrooms'].astype( int64 )
print(data.head(2))
print(data.dtypes)

# String -> Data
# data['date'] = pd.to_datetime(data['date'])
print(data.head(2))
print(data.dtypes)


# =============================================
# Criando Novas Variáveis (Colunas) no Dataset
# =============================================

data = pd.read_csv('datasets/kc_house_data.csv')
data['nome_do_pedro'] = 'Pedro'
data['comunidade_ds'] = 80
data['abertura_comunidade_ds'] = pd.to_datetime('2020-02-08')

print(data.head(2))
print(data.columns)


# ====================================================
# Excluindo (Dropando) Variáveis (Colunas) no Dataset
# ====================================================

data = data.drop('nome_do_pedro', axis=1)
cols = ['comunidade_ds', 'abertura_comunidade_ds']
data.drop(cols, axis=1, inplace=True)

print(data.head(2))
print(data.columns)


# ====================================================
# Excluindo (Dropando) Variáveis (Colunas) no Dataset
# ---------------------------------------------------
#
# Forma 1: Direto Pelo Nome da coluna
# ====================================================

data = pd.read_csv('datasets/kc_house_data.csv')
cols = ['id', 'price', 'date']
print( data[cols] )


# ===========================================
# Forma 2: Pelos Indices da Linhas e Colunas
# ===========================================

# Dataset[linhas, colunas]
print( data.iloc[0:5, 0:3] )


# ====================================================
# Forma 3: Pelos Indices da Linhas e Nome das Colunas
# =====================================================

# Dataset[linhas, colunas]
cols = ['id', 'price', 'date']
print( data.loc[0:5, cols] )


# ====================================================
# Forma 4: Pelos Indices Booleanos das Colunas
# =====================================================

# Dataset[linhas, colunas]
cols = [True, False, True, True, False, False, False, False, False,
        False, False, False, False, False, False, False, False,
        False, False, False, False]

print( data.loc[0:5, cols] )