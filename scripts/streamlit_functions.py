import streamlit      as st
import pandas as pd

from . import data_functions as defs


def create_sidebar(dataframe):
    st.sidebar.title('Dataframe Options')

    selected_attributes = st.sidebar.multiselect('Choose Columns', dataframe.columns)
    
    selected_zipcodes = st.sidebar.multiselect('Choose Zipcode', dataframe['zipcode'].unique())

    return selected_zipcodes, selected_attributes


def overview_data_section(dataframe):
    f_zipcodes, f_attributes = create_sidebar(dataframe)

    st.title('Data Overview')

    df = defs.filter_data(dataframe, f_attributes, f_zipcodes)

    st.dataframe(df)

    # c1, c2 = st.columns((1, 1.5))

    # df1 = df[['id', 'zipcode']].groupby('zipcode').count().reset_index()
    # df2 = df[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
    # df3 = df[['sqft_living', 'zipcode']].groupby('zipcode').mean().reset_index()
    # df4 = df[['price_m2', 'zipcode']].groupby('zipcode').mean().reset_index()

    # m1 = pd.merge(df1, df2, on='zipcode', how='inner')
    # m2 = pd.merge(m1, df3, on='zipcode', how='inner')
    # df = pd.merge(m2, df4, on='zipcode', how='inner')

    # df.columns = ['zipcode', 'total_houses', 'price', 'sqft_living', 'price_m2']

    # c1.header('Average Values')
    # c1.dataframe(df)

    # num_atributes = data.select_dtypes(include=['int64', 'float64'])

    # mean = pd.DataFrame(num_atributes.apply(np.mean))
    # median = pd.DataFrame(num_atributes.apply(np.median))
    # std = pd.DataFrame(num_atributes.apply(np.std))
    # min_ = pd.DataFrame(num_atributes.apply(np.min))
    # max_ = pd.DataFrame(num_atributes.apply(np.max))

    # df1 = pd.concat([max_, min_, mean, median, std], axis=1).reset_index()

    # df1.columns = ['attributes', 'max', 'min', 'mean', 'median', 'std']

    # c2.header('Descriptive Analysis')
    # c2.dataframe(df1)

    return None