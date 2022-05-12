import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import folium
import geopandas

from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

# A funcao abaixo faz com que todos elementos desenhados na tela
# ocupem a tamanho maximo disponivel
st.set_page_config(layout='wide')

# A anotcao abaixo faz com que sempre que o arquivo .csv
# seja lido, ele seja lido do cache, dando performance para
# a aplicacao. Alem disso, o parametro 'allow_output_mutation=True'
# permite com que o arquivo seja mutavel
@st.cache(allow_output_mutation=True)
def load_dataset(path):
    return pd.read_csv(path)

# Get Data
data = load_dataset('datasets/kc_house_data.csv')

# Get Geofile
path = './datasets/Zip_Codes.geojson'
geofile = geopandas.read_file(path)

# Adicionando novas features.
data['price_m2'] = data['price'] / (data['sqft_lot'] * 0.092903)

# Data Overview
# =============
#
# Essa secao disponibilizara para o CEO os filtros das colunas que
# ele desejar visualizar na tabela. O atributo criado 'f_attributes'
# possui o prefixo 'f_' para explicitar que esse atributo eh um
# atributo de filtro

# Cria um Titulo para os Filtros
st.sidebar.title('Dataframe Options')

f_attributes = st.sidebar.multiselect('Choose Columns', data.columns)
f_zipcodes = st.sidebar.multiselect('Choose Zipcode', data['zipcode'].unique())

# Adicionando um titulo para a secao
st.title('Data Overview')


# Definindo quais atributos serao exibidos
# Solicitacoes 1 e 2
# Se f_attributes e f_zipcodes estiverem difinidos
#   Selecionar linhas e colunas
# Se somente f_attributes estiver definido
#   Selecionar somente as colunas
# Se somente f_zipcodes estiver definido
#   Selecionar somente as linhas
# Se nenhum filtro estiver definido
#   Mostrar dataset original

if ( f_attributes != []) & (f_zipcodes != []):
    data = data.loc[data['zipcode'].isin(f_zipcodes), f_attributes]
elif ( f_attributes != []) & (f_zipcodes == []):
    data = data.loc[:, f_attributes]
elif ( f_attributes == []) & (f_zipcodes != []):
    data = data.loc[data['zipcode'].isin(f_zipcodes), :]
else:
    data = data.copy()

st.dataframe(data)

# Creating Streamlit Columns
# A funcão ´beta_clumns´ recebe um tuple com a quantidade de
# colunas que serao desenhadas na tela. Caso uma das colunas
# necessitar ser maior que a outra, basta passarmos um valor
# maior para a coluna em questao, conforme comando abaixo
c1, c2 = st.beta_columns((1, 1.5))

# Average Metrics
df1 = data[['id', 'zipcode']].groupby('zipcode').count().reset_index()
df2 = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
df3 = data[['sqft_living', 'zipcode']].groupby('zipcode').mean().reset_index()
df4 = data[['price_m2', 'zipcode']].groupby('zipcode').mean().reset_index()

# Merge Average Metrics
m1 = pd.merge(df1, df2, on='zipcode', how='inner')
m2 = pd.merge(m1, df3, on='zipcode', how='inner')
df = pd.merge(m2, df4, on='zipcode', how='inner')

# Rename DF indexes
df.columns = ['zipcode', 'total_houses', 'price', 'sqft_living', 'price_m2']

# Exibindo o Dataset ao CEO
c1.header('Average Values')
c1.dataframe(df)

# Statistic Descriptive
# Selecionando somente as colunas numericas
num_atributes = data.select_dtypes(include=['int64', 'float64'])

mean = pd.DataFrame(num_atributes.apply(np.mean))
median = pd.DataFrame(num_atributes.apply(np.median))
std = pd.DataFrame(num_atributes.apply(np.std))
min_ = pd.DataFrame(num_atributes.apply(np.min))
max_ = pd.DataFrame(num_atributes.apply(np.max))

df1 = pd.concat([max_, min_, mean, median, std], axis=1).reset_index()

df1.columns = ['attributes', 'max', 'min', 'mean', 'median', 'std']

c2.header('Descriptive Analysis')
c2.dataframe(df1)


# Densidade de Portifólio
# =======================
#
# Essa secao disponibilizara para o CEO um mapa para que ele possa
# visualizar a quantidade de imóvies disponíveis por região

st.title('Region Overview')

c1, c2 = st.beta_columns((1, 1))
c1.header('Portifolio Density')

# Retirando uma amostra do Dataset Original para
# agilizar na criacao do mapa
df = data.sample(100)

# Base Map - Folium labriry
# Sera utilizado a biblioteca folium para desenhar o mapa
density_map = folium.Map(location=[data['lat'].mean(), data['long'].mean()], default_zoom_start=15)

# Criando um MarkerCluster no mapa de densidade, nos
# possibilitara adicionar marcadores em nosso mapa
marker_cluster = MarkerCluster().add_to(density_map)

# Adicionando marcadores no mapa
for name, row in df.iterrows():
    folium.Marker([row['lat'], row['long']],
                  popup='Sold R${0} on: {1}. Features: {2} sqft, {3} bedrooms, {4} bathrooms, year built: {5}'
                         .format(row['price'], row['date'], row['sqft_living'], row['bedrooms'], row['bathrooms'],
                                 row['yr_built'])).add_to(marker_cluster)


with c1:
    folium_static(density_map)


# Region Price Map
c2.header('Price Density')

df = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
df.columns = ['zip', 'mean_price']

df = df.sample(10)

# Pegando somente os ZIP do Geofile que existem no dataset
geofile = geofile[geofile['ZIP'].isin(df['zip'].tolist())]

region_price_map = folium.Map(location=[data['lat'].mean(), data['long'].mean()], default_zoom_start=15)

region_price_map.choropleth(
    data=df,
    geo_data=geofile,
    columns=['zip', 'mean_price'],
    key_on='feature.properties.ZIP',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='AVG Price'
)

with c2:
    folium_static(region_price_map)


# Distribuicao de Imoveis por Categoria Comercial
# ===============================================

# Cria Filtro na Barra Lateria para Secao
st.sidebar.title('Commercial Options')

# Title
st.title('Commercial Attributes')

# Converting Date Data
data['date'] = pd.to_datetime(data['date']).dt.strftime('%Y-%m-%d')

# ------ Avg Price per Year
# Header
st.header('Avg Price per Year')

# Filtering
min_yr_built = int(data['yr_built'].min())
max_yr_built = int(data['yr_built'].max())

st.sidebar.subheader('Select Max Year Built')
f_yr_built = st.sidebar.slider('Year Built', min_yr_built, max_yr_built, int(data['yr_built'].mean()))


# Data Selection
df = data.loc[data['yr_built'] < f_yr_built]
df = df[['yr_built', 'price']].groupby('yr_built').mean().reset_index()

# Plot
fig = px.line(df, x='yr_built', y='price')
st.plotly_chart(fig, use_container_width=True)

# ------ Avg Price per Day
# Header
st.header('Avg Price per Day')

# Filtering
min_date = datetime.strptime(data['date'].min(), '%Y-%m-%d')
max_date = datetime.strptime(data['date'].max(), '%Y-%m-%d')

st.sidebar.subheader('Select Max Date')
f_date = st.sidebar.slider('Date', min_date, max_date, datetime.strptime('2014-12-01', '%Y-%m-%d'))

# Data Selection
data['date'] = pd.to_datetime(data['date'])
df = data.loc[data['date'] < f_date]
df = df[['date', 'price']].groupby('date').mean().reset_index()

# Plot
fig = px.line(df, x='date', y='price')
st.plotly_chart(fig, use_container_width=True)


# Histograma
# ==========

# --- Price Distribution
# --- ==================
st.title('Distributions')
st.header('Price Distribution')

st.sidebar.title('Distributions')
st.sidebar.subheader('Select Max Price')

# Filters
min_price = int(data['price'].min())
max_price = int(data['price'].max())
mean_price = int(data['price'].mean())

f_price = st.sidebar.slider('Price', min_price, max_price, mean_price)

# Data Selection
df = data.loc[data['price'] < f_price]

# Plot
fig = px.histogram(df, x='price', nbins=50)
st.plotly_chart(fig, use_container_width=True)

# --- Distribution per Physical Features
# --- ==================================

# Filtes
st.sidebar.subheader('Select Max Bedrooms')
f_bedrooms = st.sidebar.selectbox('Max Number of Bedrooms', sorted(set(data['bedrooms'].unique())))

st.sidebar.subheader('Select Max Bathrooms')
f_bathrooms = st.sidebar.selectbox('Max Number of Bathrooms', sorted(set(data['bathrooms'].unique())))

st.sidebar.subheader('Select Max Floors')
f_bathrooms = st.sidebar.selectbox('Max Number of Floors', sorted(set(data['floors'].unique())))

st.sidebar.subheader('Has Water View?')
f_waterview = st.sidebar.checkbox('Yes')


# Columns
c1, c2 = st.beta_columns((1, 1))

# Selecting Data - House per bedrooms
c1.header('Houses per Bedrooms')
df = data[data['bedrooms'] < f_bedrooms]

# Plot - House per bedrooms
fig = px.histogram(df, x='bedrooms', nbins=19)
c1.plotly_chart(fig, use_container_width=True)


# Selecting Data - House per bathrooms
c2.header('Houses per Bathrooms')
df = data[data['bathrooms'] < f_bathrooms]

# Plot - House per bathrooms
fig = px.histogram(df, x='bathrooms', nbins=19)
c2.plotly_chart(fig, use_container_width=True)


# Columns
c1, c2 = st.beta_columns((1, 1))

# Selecting Data - House per floors
c1.header('Houses per Floors')
df = data[data['floors'] < f_bedrooms]

# Plot - House per bedrooms
fig = px.histogram(df, x='floors', nbins=19)
c1.plotly_chart(fig, use_container_width=True)


# Selecting Data - House per water view
c2.header('Houses per Waterview')
if f_waterview:
    df = data[data['waterfront'] == 1]
else:
    df = data.copy()

# Plot - House per bedrooms
fig = px.histogram(df, x='waterfront', nbins=10)
c2.plotly_chart(fig, use_container_width=True)