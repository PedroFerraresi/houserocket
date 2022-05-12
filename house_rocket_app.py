# App que irá criar o Mapa Interativo com Streamlit
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

st.title('House Rocket Company')
st.markdown('Welcome to House Rocket Data Analysis')
st.header('Load Data')

# Read Data
@st.cache(allow_output_mutation=True)
def get_data(path):
    data = pd.read_csv(path)
    data['date'] = pd.to_datetime(data['date'])

    return data

# Load Data
data = get_data('datasets/kc_house_data.csv')


# Filter bedrooms
bedrooms = st.sidebar.multiselect('Number of Bedrooms', data['bedrooms'].unique())

st.write('Your filter is: ', bedrooms[0])

# Plot Map
st.title('House Rocket Map')
is_checked = st.checkbox('Display Map')

# Filter
price_min = int(data['price'].min())
price_max = int(data['price'].max())
price_avg = int(data['price'].mean())

price_slider = st.slider('Price Range', price_min, price_max, price_avg)

# Condition to see the Map
if is_checked:
    # Rows Selection
    houses = data[data['price'] < price_slider][['id', 'lat', 'long', 'price']]

    # Showing dataset
    st.dataframe(houses)

    fig = px.scatter_mapbox(houses, lat='lat', lon='long', size='price',
                            color_continuous_scale=px.colors.cyclical.IceFire,
                            size_max=15, zoom=10)

    # Adjusting Map layout
    fig.update_layout(mapbox_style='open-street-map')
    fig.update_layout(height=600, margin={'r': 0, 'b': 0, 'l': 0, 't': 0})
    st.plotly_chart(fig)