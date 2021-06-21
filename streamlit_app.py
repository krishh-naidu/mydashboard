
from numpy.lib.histograms import histogram
import streamlit as st
import numpy as np
import pandas as pd
from streamlit.proto.Slider_pb2 import Slider
from dataload import df
import pydeck as pdk
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px 

# Use the full page instead of a narrow central column
st.set_page_config(layout="wide")


st.title('Coutries GEO Data')
"""
Here's our first attempt at using data to create a table:
"""
map_data = df.copy()
map_data["lat"] = pd.to_numeric(map_data["lat"],downcast='float')
map_data["lon"] = pd.to_numeric(map_data["lon"],downcast='float')
map_data = map_data.dropna()

if st.sidebar.checkbox('Show Countries Dataframe'):
    df
    st.write('There are total',df['Name'].count(), 'Countries')

if st.sidebar.checkbox('Show World Map'):
    st.map(map_data)

if st.sidebar.checkbox('Show Countries LatLng Data'):
    st.write((map_data[['Name','lat','lon']]))



# Space out the maps so the first one is 2x the size of the other three
c1, c2, c3, c4 = st.beta_columns((2, 1, 1, 1))


Region_option=st.sidebar.selectbox(
    'Select Regions',
    map_data['Region'].unique())

if Region_option=='Asia' or 'Europe' or 'Africa' or 'Oceania' or 'Americas' or 'Polar':
    st.write('Total Countries in',Region_option)
    region_df = map_data[map_data['Region']==Region_option]
    st.write(region_df.reset_index(drop=True)) # to reset the index for resulted df
    st.write('there are total', region_df['Name'].count(),'Countries')
    st.map(region_df[['lat','lon']])


# Create a sidebar
option = st.sidebar.selectbox(
    'Which country you want to see?',
    df['Name'])


df1 = map_data[map_data['Name']==option]
#st.map(df1)
lat = int(df1['lat'])
lon=int(df1['lon'])

st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v10',
     
     initial_view_state=
     pdk.ViewState(
         latitude=lat,
         longitude=lon,
         zoom=5,
         pitch=50,
     ),
     layers=[
        pdk.Layer(
           'HexagonLayer',
           data=df1,
           radius=300,
           auto_highlight=True,
           elevation_scale=50,
           elevation_range=[0, 3000],
            pickable=True,
            extruded=True,
         ),
         pdk.Layer(
             'ScatterplotLayer',
             data=df1,
             get_position='[lat, lon]',
             #get_fill_color='[COLORS_R, COLORS_G, COLORS_B]',
             get_radius=200,
         ),
     ],
 ))

'You selected:', option

# Charts code
hist_data=[]
labels=[]
chart_data = region_df[['Name','Population']].copy().reset_index(drop=True)
#st.bar_chart(chart_data)
hist_data.append(chart_data['Population'].to_numpy().tolist())
labels.append(chart_data['Name'].to_string())

if st.sidebar.checkbox('Population BAR Chart by Region'):
    # bar chart
    fig = go.Figure(
        data=[go.Bar(x=chart_data['Name'],y=chart_data['Population'])],
        layout_title_text=Region_option + ' ' + 'Population Chart'
    )
    fig.update_layout(width=1000,height=900)
    st.plotly_chart(fig)


# line chart
if st.sidebar.checkbox('Population LINE Chart by Region'):
    fig = px.line(x=chart_data['Name'],y=chart_data['Population'],
        title=Region_option + ' ' + 'Population Line Chart'
        )
    fig.update_layout(width=1000,height=900)
    st.plotly_chart(fig)

# funnel chart
if st.sidebar.checkbox('Population FUNNEL Chart by Region'):
    data = dict(
        number=chart_data['Population'],
        stage=chart_data['Name'])
    fig = px.funnel(data, x='number', y='stage')
    fig.update_layout(width=1100,height=900)
    st.plotly_chart(fig)

# Pie Chart
if st.sidebar.checkbox('Population PIE Chart by Region'):
    fig = px.pie(chart_data, values='Population', names='Name', title='Population of' +Region_option+ 'continent')
    fig.update_layout(width=1100,height=1000)
    st.plotly_chart(fig)


#st.write(map_data)
# Sunburst Chart
# colors: 'aggrnyl', 'agsunset', 'algae', 'amp', 'armyrose', 'balance', 'blackbody', 'bluered', 'blues', 'blugrn', 'bluyl', 'brbg', 'brwnyl', 'bugn', 'bupu', 'burg', 'burgyl', 'cividis', 'curl', 'darkmint', 'deep', 'delta', 'dense', 'earth', 'edge', 'electric', 'emrld', 'fall', 'geyser', 'gnbu', 'gray', 'greens', 'greys', 'haline', 'hot', 'hsv', 'ice', 'icefire', 'inferno', 'jet', 'magenta', 'magma', 'matter', 'mint', 'mrybm', 'mygbm', 'oranges', 'orrd', 'oryel', 'oxy', 'peach', 'phase', 'picnic', 'pinkyl', 'piyg', 'plasma', 'plotly3', 'portland', 'prgn', 'pubu', 'pubugn', 'puor', 'purd', 'purp', 'purples', 'purpor', 'rainbow', 'rdbu', 'rdgy', 'rdpu', 'rdylbu', 'rdylgn', 'redor', 'reds', 'solar', 'spectral', 'speed', 'sunset', 'sunsetdark', 'teal', 'tealgrn', 'tealrose', 'tempo', 'temps', 'thermal', 'tropic', 'turbid', 'turbo', 'twilight', 'viridis', 'ylgn', 'ylgnbu', 'ylorbr', 'ylorrd'
if st.sidebar.checkbox('Population Sunburst Chart by Region'):
    map_data = map_data[map_data['Population'] > 0]
    fig = px.sunburst(map_data, path=['Region', 'Name'],
    values='Population', names='Name', title='Population of' +Region_option+ 'continent',
    color='Population',hover_data=['Name'],
    color_continuous_scale='deep',
    color_continuous_midpoint=np.average(map_data['Population'], weights=map_data['Population'])
    )
    fig.update_layout(width=900,height=1000)
    st.plotly_chart(fig)

# Plotly Map
df = px.data.gapminder().query("year==2007").reset_index(drop=True)
#st.write(df)
if st.sidebar.checkbox('Select Coutry Map'):
    if Region_option=='Asia' or 'Europe' or 'Africa' or 'Oceania' or 'Americas' or 'Polar':
        st.write('Total Countries in',Region_option)
        df = df[df['continent']==Region_option]
        fig = px.choropleth(df, locations="iso_alpha", 
                        color="pop", hover_name="country",
                        color_continuous_scale=px.colors.sequential.Viridis,scope=Region_option.lower(),
                        #mapbox_style="carto-positron"
                        )
        fig.update_layout(width=1000,height=300,margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig)

df = px.data.gapminder().reset_index(drop=True)

years_to_filter = st.slider('Years',min_value=1952,max_value=2007,step=5)
if Region_option=='Asia' or 'Europe' or 'Africa' or 'Oceania' or 'Americas' or 'Polar':
    df = df[df['continent']==Region_option]
    df = df[df['year']==years_to_filter].reset_index(drop=True)
    fig = px.choropleth(df, locations="iso_alpha", 
                            color="pop", hover_name="country",
                            color_continuous_scale=px.colors.sequential.deep,scope=Region_option.lower(),
                            #mapbox_style="carto-positron"
                            )
fig.update_layout(width=1000,height=300,margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig) 

df = px.data.gapminder().reset_index(drop=True)
df = df[df['continent']==Region_option]
df
fig = px.bar(
    df,x='year',y='pop',
    title='Population growth for' + ' ' + Region_option + ' ' + '1952 - 2007',
    color= 'pop')
st.plotly_chart(fig)

from plotly.subplots import make_subplots
df = px.data.gapminder().reset_index(drop=True)
df = df[df['country']==option]
fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(
    go.Scatter(x=df['year'], y=df['pop'], name="Population"),
    row=1, col=1, secondary_y=False)

fig.add_trace(
    go.Scatter(x=df['year'], y=df['gdpPercap'], name="GDP"),
    row=1, col=1, secondary_y=True,
)
# Set x-axis title
fig.update_xaxes(title_text="<b>Years</b>")

# Set y-axes titles
fig.update_yaxes(title_text="<b>Population</b>", secondary_y=False)
fig.update_yaxes(title_text="<b>GDP Per Capita</b>", secondary_y=True)
fig.update_layout(width=800,height=700)
st.plotly_chart(fig)