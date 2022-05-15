import streamlit as st
from streamlit_folium import folium_static
import pandas as pd
import folium
# from folium import plugins

def mapplot(df):
    map1 = folium.Map(
        location=[df['latitude'].iloc[0], df['longitude'].iloc[0]],
        tiles='cartodbpositron',
        zoom_start=12,
    )
    for index, row in df.iterrows():
        folium.Marker([row['latitude'], row['longitude']], 
        popup="<a href='https://www.google.com/maps/search/"+row['address']+"' target='_blank'>"+row['address']+"</a> - <a href='"+row['url']+"' target='_blank'>details</a>",
        tooltip=row['price']+" "+row['bedrooms']+" "+row['bathrooms']+" "+str(row['surface'])
        ).add_to(map1)
    return map1

# @st.cache
def load_data():
    df = pd.read_csv("boston.csv",index_col=None)
    return df

df = load_data()

st.title("🏠 Boston")

map1 = mapplot(df)
folium_static(map1)