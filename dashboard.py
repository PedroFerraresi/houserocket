import os
import folium
import geopandas

import streamlit      as st
import pandas         as pd
import numpy          as np
import plotly.express as px

from datetime          import datetime
from folium.plugins    import MarkerCluster
from streamlit_folium  import folium_static

from scripts           import data_functions      as defs
from scripts           import streamlit_functions  as stf

st.set_page_config(layout='wide')


def portifolio_desinty(data, geofile):
    st.title('Region Overview')

    c1, c2 = st.columns((1, 1))
    c1.header('Portifolio Density')

    df = data.sample(100)

    density_map = folium.Map(location=[data['lat'].mean(), data['long'].mean()], default_zoom_start=15)

    marker_cluster = MarkerCluster().add_to(density_map)

    for name, row in df.iterrows():
        folium.Marker([row['lat'], row['long']],
                      popup='Sold R${0} on: {1}. Features: {2} sqft, {3} bedrooms, {4} bathrooms, year built: {5}'
                      .format(row['price'],
                              row['date'],
                              row['sqft_living'],
                              row['bedrooms'],
                              row['bathrooms'],
                              row['yr_built'])
                      ).add_to(marker_cluster)

    with c1:
        folium_static(density_map)

    c2.header('Price Density')

    df = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
    df.columns = ['zip', 'mean_price']

    df = df.sample(10)

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

    return None


def comercial(data):
    st.sidebar.title('Commercial Options')

    st.title('Commercial Attributes')

    data['date'] = pd.to_datetime(data['date']).dt.strftime('%Y-%m-%d')

    st.header('Avg Price per Year')

    min_yr_built = int(data['yr_built'].min())
    max_yr_built = int(data['yr_built'].max())

    st.sidebar.subheader('Select Max Year Built')
    f_yr_built = st.sidebar.slider('Year Built', min_yr_built, max_yr_built, int(data['yr_built'].mean()))

    df = data.loc[data['yr_built'] < f_yr_built]
    df = df[['yr_built', 'price']].groupby('yr_built').mean().reset_index()

    fig = px.line(df, x='yr_built', y='price')
    st.plotly_chart(fig, use_container_width=True)

    st.header('Avg Price per Day')

    min_date = datetime.strptime(data['date'].min(), '%Y-%m-%d')
    max_date = datetime.strptime(data['date'].max(), '%Y-%m-%d')

    st.sidebar.subheader('Select Max Date')
    f_date = st.sidebar.slider('Date', min_date, max_date, datetime.strptime('2014-12-01', '%Y-%m-%d'))

    data['date'] = pd.to_datetime(data['date'])
    df = data.loc[data['date'] < f_date]
    df = df[['date', 'price']].groupby('date').mean().reset_index()

    fig = px.line(df, x='date', y='price')
    st.plotly_chart(fig, use_container_width=True)

    return None


def attributes_distributions(data):
    # --- Price Distribution
    # --- ==================
    st.title('Distributions')
    st.header('Price Distribution')

    st.sidebar.title('Distributions')
    st.sidebar.subheader('Select Max Price')

    min_price = int(data['price'].min())
    max_price = int(data['price'].max())
    mean_price = int(data['price'].mean())

    f_price = st.sidebar.slider('Price', min_price, max_price, mean_price)

    df = data.loc[data['price'] < f_price]

    fig = px.histogram(df, x='price', nbins=50)
    st.plotly_chart(fig, use_container_width=True)

    # --- Distribution per Physical Features
    # --- ==================================
    st.sidebar.subheader('Select Max Bedrooms')
    f_bedrooms = st.sidebar.selectbox('Max Number of Bedrooms', sorted(set(data['bedrooms'].unique())))

    st.sidebar.subheader('Select Max Bathrooms')
    f_bathrooms = st.sidebar.selectbox('Max Number of Bathrooms', sorted(set(data['bathrooms'].unique())))

    st.sidebar.subheader('Select Max Floors')
    f_floors = st.sidebar.selectbox('Max Number of Floors', sorted(set(data['floors'].unique())))

    st.sidebar.subheader('Has Water View?')
    f_waterview = st.sidebar.checkbox('Yes')

    c1, c2 = st.columns((1, 1))

    c1.header('Houses per Bedrooms')
    df = data[data['bedrooms'] < f_bedrooms]

    fig = px.histogram(df, x='bedrooms', nbins=19)
    c1.plotly_chart(fig, use_container_width=True)

    c2.header('Houses per Bathrooms')
    df = data[data['bathrooms'] < f_bathrooms]

    fig = px.histogram(df, x='bathrooms', nbins=19)
    c2.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns((1, 1))

    c1.header('Houses per Floors')
    df = data[data['floors'] <= f_floors]

    fig = px.histogram(df, x='floors', nbins=19)
    c1.plotly_chart(fig, use_container_width=True)

    c2.header('Houses per Waterview')
    if f_waterview:
        df = data[data['waterfront'] == 1]
    else:
        df = data.copy()

    fig = px.histogram(df, x='waterfront', nbins=10)
    c2.plotly_chart(fig, use_container_width=True)

    return None


if __name__ == '__main__':
    # ETL
    # Extraction
    if os.path.isfile('./datasets/Zip_Codes.geojson'):
        geo_data = geopandas.read_file('./datasets/Zip_Codes.geojson')

        if os.path.isfile('datasets/kc_house_data.csv'):
            df = defs.load_dataset('datasets/kc_house_data.csv')

            # Creating Overview Data Section
            stf.overview_data_section(df)

            # # Creating Portifolio Density Section
            # portifolio_desinty(df, geo_data)

            # # Creating Commercial Section
            # comercial(df)

            # # Creating Distributions
            # attributes_distributions(df)

        else:
            st.title('CSV File is missing.')
    else:
        st.title('GEO Data File is missing.')

