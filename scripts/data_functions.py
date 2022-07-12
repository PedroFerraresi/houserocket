from pyparsing import col
import streamlit      as st
import pandas         as pd


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


def filter_data(dataframe, columns, zipcodes):

    df = dataframe.copy()

    if (columns != []) & (zipcodes != []):
        return df.loc[df['zipcode'].isin(zipcodes), columns]

    elif (columns != []) & (zipcodes == []):
        return df.loc[:, columns]
    
    elif (columns == []) & (zipcodes != []):
        return df.loc[df['zipcode'].isin(zipcodes), :]
    
    else:
        return df.copy()

