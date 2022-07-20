import streamlit  as st

def create_data_overview_filter(dataframe):
    df = dataframe.copy()

    selected_attributes = st.sidebar.multiselect('Choose Columns', df.columns)

    selected_zipcodes = st.sidebar.multiselect('Choose Zipcode', df['zipcode'].unique())

    overview = {
        'selected_attributes': selected_attributes,
        'selected_zipcodes': selected_zipcodes,
    }

    return overview


def create_sidebar(dataframe):
    st.sidebar.title('Data Overview Filters')

    overview = create_data_overview_filter(dataframe)

    return overview

