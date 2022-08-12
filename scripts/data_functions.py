from pyparsing import col

import streamlit      as st
import pandas         as pd
import numpy          as np


@st.cache(allow_output_mutation=True)
def load_dataset(path):
    """Create DataFrame object based on .csv file

    Parameters
    ----------
    path : str
        File path.

    Return
    ------
    pandas.DataFrame
        DataFrame object with .csv data.
    """
    dataframe = pd.read_csv(path)

    dataframe['date'] = dataframe['date'].apply(lambda x: x.split('T')[0])

    dataframe['date'] = pd.to_datetime(dataframe['date']).dt.date
    
    dataframe = dataframe.loc[dataframe['bedrooms'] > 0, :]
    dataframe = dataframe.loc[dataframe['bedrooms'] < 33, :]
    dataframe = dataframe.loc[dataframe['bathrooms'] > 0, :]
    
    dataframe = dataframe.drop_duplicates()

    return create_price_m2_feature(dataframe)


@st.cache(allow_output_mutation=True)
def create_price_m2_feature(dataframe):
    """Create price_m2 column

    Parameters
    ----------
    data : pandas.DataFrame
        DataFrame with data needed to create price_m2 column.

    Return
    ------
    pandas.DataFrame
        DataFrame object with price_m2 created
    """
    dataframe['price_m2'] = dataframe['price'] / (dataframe['sqft_lot'] * 0.092903)

    return dataframe


def filter_data(dataframe, columns = None, zipcodes = None):

    df = dataframe.copy()

    if columns is None:
        columns = []

    if zipcodes is None:
        zipcodes = []

    if (columns != []) & (zipcodes != []):
        return df.loc[df['zipcode'].isin(zipcodes), columns]

    elif (columns != []) & (zipcodes == []):
        return df.loc[:, columns]
    
    elif (columns == []) & (zipcodes != []):
        return df.loc[df['zipcode'].isin(zipcodes), :]
    
    else:
        return df.copy()



def create_avg_dataframe(dataframe):
    df = dataframe.copy()
    
    df_qty_houses = df[['id', 'zipcode']].groupby('zipcode').count().reset_index()
    df_price = df[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
    df_sqft_living = df[['sqft_living', 'zipcode']].groupby('zipcode').mean().reset_index()
    df_m2_price = df[['price_m2', 'zipcode']].groupby('zipcode').mean().reset_index()

    m1 = pd.merge(df_qty_houses, df_price, on='zipcode', how='inner')
    m2 = pd.merge(m1, df_sqft_living, on='zipcode', how='inner')
    df_final = pd.merge(m2, df_m2_price, on='zipcode', how='inner')

    df_final.columns = ['zipcode', 'total_houses', 'price', 'sqft_living', 'price_m2']

    return df_final


def create_num_features_df(dataframe):
    df = dataframe.copy()

    df_num_atributes = df.select_dtypes(include=['int64', 'float64'])

    drop_columns = ['id', 'waterfront', 'view', 'condition', 'zipcode', 'floors', 'grade', 'lat', 'long']

    df_num_atributes = df_num_atributes.drop(drop_columns, axis=1)

    std    = pd.DataFrame(df_num_atributes.apply(np.std))
    min_   = pd.DataFrame(df_num_atributes.apply(np.min))
    max_   = pd.DataFrame(df_num_atributes.apply(np.max))
    mean   = pd.DataFrame(df_num_atributes.apply(np.mean))
    median = pd.DataFrame(df_num_atributes.apply(np.median))

    df_final = pd.concat([max_, min_, mean, median, std], axis=1).reset_index()

    df_final.columns = ['attributes', 'max', 'min', 'mean', 'median', 'std']

    return df_final