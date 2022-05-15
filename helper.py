import pandas as pd
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