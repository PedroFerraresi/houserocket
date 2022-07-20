import folium
import streamlit      as st
import plotly.express as px
from datetime          import datetime


def create_sidebar_avg_price_year_filter(data):
    st.sidebar.subheader('Select Years Range')

    values = data["yr_built"].unique().tolist()

    values.sort()

    min_year, max_year = st.sidebar.select_slider(
        'Select the Years to filter the Avg Price per Year',
        options=values,
        value=(int(data['yr_built'].median()), int(data['yr_built'].max()))
    )

    return min_year, max_year


def create_avg_price_day_filter(data):
    st.sidebar.subheader('Select Days Range')

    f_min_date = data['date'].min()

    f_max_date = data['date'].max()

    values = data["date"].unique().tolist()

    values.sort()

    min_date, max_date = st.sidebar.select_slider(
        'Select Dates to filter the Avg Price per Day',
        options=values,
        value=(f_min_date, f_max_date)
    )

    return min_date, max_date



def create_avg_price_per_year_plot(data):
    min_year, max_year = create_sidebar_avg_price_year_filter(data)

    df = data.loc[(data['yr_built'] >= min_year) & (data['yr_built'] <= max_year), :]
    
    df = df[['yr_built', 'price']].groupby('yr_built').mean().reset_index()

    fig = px.line(df, x='yr_built', y='price')

    st.plotly_chart(fig, use_container_width=True)

    return None


def create_avg_price_per_day_plot(data):
    min_date, max_date = create_avg_price_day_filter(data)
    
    df = data.loc[(data['date'] >= min_date) & (data['date'] <= max_date), :]

    df = df[['date', 'price']].groupby('date').mean().reset_index()

    fig = px.line(df, x='date', y='price')

    st.plotly_chart(fig, use_container_width=True)

    return None
