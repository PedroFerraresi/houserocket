from os import ctermid
import streamlit  as st

from streamlit_folium  import folium_static

from . import data_functions            as defs
from . import st_data_overview          as dto
from . import st_region_overview        as rgo
from . import st_commercial_attributes  as cat
from . import st_distributions_overview as dio


def create_overview_data_section(dataframe):
    df = dataframe.copy()

    sidebar_filters = dto.create_sidebar(dataframe)

    st.title('Data Overview')

    df_filtered = defs.filter_data(
        dataframe, 
        sidebar_filters['selected_attributes'], 
        sidebar_filters['selected_zipcodes']
    )

    st.dataframe(df_filtered)

    c1, c2 = st.columns((1, 1.5))

    df_avg_values = defs.create_avg_dataframe(df)

    df_num_features = defs.create_num_features_df(df)

    c1.header('Average Values')
    c1.dataframe(df_avg_values)

    c2.header('Descriptive Analysis')
    c2.dataframe(df_num_features)

    return None


def create_portifolio_desinty_section(data, geofile):
    st.title('Region Overview')
    
    c1, c2 = st.columns((1, 1))

    c1.header('Portifolio Density')

    density_map = rgo.create_density_map(data)

    with c1:
        folium_static(density_map)


    c2.header('Price Density')

    region_price_map = rgo.create_price_region_map(data, geofile)

    with c2:
        folium_static(region_price_map)

    return None


def create_commercial_attributes_section(data):
    st.title('Commercial Attributes')

    st.sidebar.title('Commercial Attributes Options')

    st.header('Avg Price per Year')

    cat.create_avg_price_per_year_plot(data)

    st.header('Avg Price per Day')

    cat.create_avg_price_per_day_plot(data)

    return None


def create_distribuition_overview_section(data):    
    st.title('Distributions')
    st.header('Price Distribution')
    
    # dio.createdistribuition_overview(data)