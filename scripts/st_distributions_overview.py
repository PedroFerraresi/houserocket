from operator import index, is_
import streamlit as st
import plotly.express as px

from folium.plugins    import MarkerCluster


def create_price_distribuition_filter(dataframe):
    data = dataframe.copy()
    
    # --- Price Distribution Filters
    st.sidebar.title('Distributions')
    st.sidebar.subheader('Select Price Range')
    
    f_min_price = float(data['price'].min())
    f_mean_price = float(data['price'].median())
    
    values = dataframe["price"].unique().tolist()
    
    values.sort()
    
    min_price, max_price = st.sidebar.select_slider(
        'Select Prices Range to filter prices distribuition',
        options=values,
        value=(f_min_price, f_mean_price)
    )
    
    return min_price, max_price


def create_price_distribuition_plot(dataframe, min_price, max_price):
    df = dataframe.loc[ (dataframe['price'] <= max_price) & (dataframe['price'] >= min_price) ]

    fig = px.histogram(df, x='price', nbins=50)
    st.plotly_chart(fig, use_container_width=True)
    
    return None


def create_bedrooms_bathrroms_distribuition_filter(dataframe):
    # --- Distribution per Physical Features
    # --- ==================================
    st.sidebar.subheader('Select Max Bedrooms')
    
    bedrooms_values = sorted(set(dataframe['bedrooms'].unique()))
    
    qty_bedrooms = st.sidebar.selectbox('Max Number of Bedrooms', bedrooms_values, index = len(bedrooms_values) - 1)

    st.sidebar.subheader('Select Max Bathrooms')
    
    bathroom_values = sorted(set(dataframe['bathrooms'].unique()))
    
    qty_bathrooms = st.sidebar.selectbox('Max Number of Bathrooms', bathroom_values, index = len(bathroom_values) - 1)
    
    return qty_bedrooms, qty_bathrooms


def create_bedrooms_bathrroms_distribuition_plots(dataframe, qty_bedroom, qty_bathrooms):
    c1, c2 = st.columns((1, 1))

    c1.header('Houses per Bedrooms')
    df = dataframe[dataframe['bedrooms'] <= qty_bedroom]

    fig = px.histogram(df, x='bedrooms', nbins=19)
    c1.plotly_chart(fig, use_container_width=True)

    c2.header('Houses per Bathrooms')
    df = dataframe[dataframe['bathrooms'] <= qty_bathrooms]

    fig = px.histogram(df, x='bathrooms', nbins=19)
    c2.plotly_chart(fig, use_container_width=True)
    
    return None


def create_floors_waterfront_distribuition_filters(dataframe):
    # --- Distribution per Physical Features
    # --- ==================================
    st.sidebar.subheader('Select Max Floors')
    
    floors_values = sorted(set(dataframe['floors'].unique()))
    
    qty_floors = st.sidebar.selectbox('Max Number of Floors', floors_values, index = len(floors_values) - 1)

    st.sidebar.subheader('Has Water View?')
    
    is_waterview = st.sidebar.checkbox('Yes')
    
    return qty_floors, is_waterview
    
    
    
def create_floors_waterfront_distribuition_plots(dataframe, qty_floors, is_waterview):
    c1, c2 = st.columns((1, 1))

    c1.header('Houses per Floors')
    df = dataframe[dataframe['floors'] <= qty_floors]

    fig = px.histogram(df, x='floors', nbins=19)
    c1.plotly_chart(fig, use_container_width=True)

    c2.header('Houses per Waterview')
    if is_waterview:
        df = dataframe[dataframe['waterfront'] == 1]
    else:
        df = dataframe.copy()

    fig = px.histogram(df, x='waterfront', nbins=10)
    c2.plotly_chart(fig, use_container_width=True)

    return None