import streamlit as st
from streamlit_folium import folium_static
import pandas as pd
import folium
# from folium import plugins
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

def geosearch(df):
    locator = Nominatim(user_agent="myGeocoder")
    # 1 - convenient function to delay between geocoding calls
    geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
    # 2- - create location column
    df['location'] = df['address'].apply(geocode)
    # 3 - create longitude, latitude and altitude from location column (returns tuple)
    df['point'] = df['location'].apply(lambda loc: tuple(loc.point) if loc else None)  
    # 3bis - drop NaN in point (geocoding not finding a location)
    df2 = df.dropna(subset=['point'])   
    # 4 - split point column into latitude, longitude and altitude columns
    df2[['latitude', 'longitude', 'altitude']] = pd.DataFrame(df2['point'].tolist(), index=df2.index)
    return df2

def mapplot(df):
    map1 = folium.Map(
        location=[df['latitude'].iloc[0], df['longitude'].iloc[0]],
        tiles='cartodbpositron',
        zoom_start=12,
    )
    for index, row in df.iterrows():
        folium.Marker([row['latitude'], row['longitude']], 
        popup=row['address']+" - <a href='"+row['url']+"'target='_blank'>details</a>",
        tooltip=row['price']+" "+row['bedrooms']+" "+row['bathrooms']+" "+str(row['surface'])
        ).add_to(map1)
    return map1

# @st.cache
def load_data():
    df = pd.read_csv("boston.csv",index_col=None)
    df2 = geosearch(df)
    return df2

df = load_data()

st.title("🏠 Boston")

map1 = mapplot(df)
folium_static(map1)