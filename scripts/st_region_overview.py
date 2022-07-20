import folium

from folium.plugins    import MarkerCluster

def create_density_map(data):
    df = data.sample(2000)
    
    density_map = folium.Map(location=[data['lat'].mean(), data['long'].mean()], default_zoom_start=15)

    marker_cluster = MarkerCluster().add_to(density_map)

    
    for _, row in df.iterrows():
        popup_string = f'Sold R$ {round(row["price"], 2)} on: {row["date"]}. '\
                       f'Features: {row["sqft_living"]} sqft, {row["bedrooms"]} bedrooms, '\
                       f'{row["bathrooms"]} bathrooms, year built: {row["yr_built"]}'
        
        folium.Marker( [ row['lat'], row['long'] ], popup = popup_string ).add_to(marker_cluster)

    return density_map


def create_price_region_map(data, geofile):

    df = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
    
    df_avg_price = df.rename(columns = {'zipcode': 'zip', 'price': 'mean_price'})

    geo_data = geofile[geofile['ZIP'].isin(df_avg_price['zip'].tolist())]

    region_price_map = folium.Map(location=[data['lat'].mean(), data['long'].mean()], default_zoom_start=15)

    folium.Choropleth(
        geo_data=geo_data,
        data=df_avg_price,
        columns=['zip', 'mean_price'],
        key_on='feature.properties.ZIP',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='AVG Price'
    ).add_to(region_price_map)

    return region_price_map

