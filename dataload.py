from numpy.core.arrayprint import printoptions
import requests
import json
from pprint import pprint
import pandas as pd
from IPython.core.display import HTML
import numpy as np
r = requests.get('https://restcountries.eu/rest/v2/all')

#print(json.loads(r.content))
json_res = r.json()

country_name=[]
capital_name=[]
population = []
region=[]
lat =[]
lng=[]
area=[]
borders=[]
currencies=[]
languages=[]
flag=[]
#print(type(json_res))
for i in range(len(json_res)):
    #pprint(json_res[i]['name'])
    country_name.append(json_res[i]['name'])
    capital_name.append(json_res[i]['capital'])
    population.append(json_res[i]['population'])
    region.append(json_res[i]['region'])
    lat.append(json_res[i]['latlng'][0:-1])
    lng.append(json_res[i]['latlng'][1:])
    area.append(json_res[i]['area'])
    borders.append(json_res[i]['borders'])
    currencies.append(json_res[i]['currencies'][0]['name'])

    for lang in range(len(json_res[i]['languages'])):
        languages.append([])
        languages[i].append(json_res[i]['languages'][lang]['name'])

    flag.append(json_res[i]['flag'])



data_tuples = list(zip(country_name,capital_name,population,region,lat,lng,area,borders,currencies,languages,flag))
df = pd.DataFrame(data_tuples,columns=['Name','Capital','Population','Region','lat','lon','Area','Borders','Currencies','Languages','Flag'])

# Data Cleanup

df['lat'] = [','.join(map(str, l)) for l in df['lat']]
df['lon'] = [','.join(map(str, l)) for l in df['lon']]
df['Borders'] = [','.join(map(str, l)) for l in df['Borders']]
df['Languages'] = [','.join(map(str, l)) for l in df['Languages']]

# Converting links to html tags
def path_to_image_html(path):
    return '<img src="'+ path + '" width="60" >'


# Rendering the dataframe as HTML table
df.to_html(escape=False, formatters=dict(Flag=path_to_image_html))

# Rendering the images in the dataframe using the HTML method.
HTML(df.to_html(escape=False,formatters=dict(Flag=path_to_image_html)))

# Saving the dataframe as a webpage
df.to_html('Countries.html',escape=False, formatters=dict(Flag=path_to_image_html))


