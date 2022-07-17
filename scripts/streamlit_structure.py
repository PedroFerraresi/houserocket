import streamlit  as st

from streamlit_folium  import folium_static

from . import data_overview   as dto
from . import data_functions  as defs
from . import region_overview as rgo


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