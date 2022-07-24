import streamlit as st

from folium.plugins    import MarkerCluster

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

def create_price_distribuition_filter(dataframe):
    data = dataframe.copy()
        
    min_price = float(data['price'].min())
    max_price = float(data['price'].max())
    mean_price = float(data['price'].mean())

    f_price = st.sidebar.slider('Price', min_price, max_price, mean_price)
    
    # --- Distribution per Physical Features Filters
    st.sidebar.subheader('Select Max Bedrooms')
    f_bedrooms = st.sidebar.selectbox('Max Number of Bedrooms', sorted(set(data['bedrooms'].unique())))

    st.sidebar.subheader('Select Max Bathrooms')
    f_bathrooms = st.sidebar.selectbox('Max Number of Bathrooms', sorted(set(data['bathrooms'].unique())))

    st.sidebar.subheader('Select Max Floors')
    f_floors = st.sidebar.selectbox('Max Number of Floors', sorted(set(data['floors'].unique())))

    st.sidebar.subheader('Has Water View?')
    f_waterview = st.sidebar.checkbox('Yes')
    
    return None


def create_distribuition_sidebar(dataframe):
    # --- Price Distribution Filters
    st.sidebar.title('Distributions')
    st.sidebar.subheader('Price Range')
    
    create_price_distribuition_filter



def create_distribuition_overview(dataframe):
    data = dataframe.copy()
    
    df = data.loc[data['price'] < f_price]

    fig = px.histogram(df, x='price', nbins=50)
    st.plotly_chart(fig, use_container_width=True)

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
