import requests
import json
from dotenv import load_dotenv
import os
import pandas as pd
from pymongo import MongoClient
from pandas import json_normalize
from pymongo import MongoClient,GEOSPHERE
import shapely.geometry
import geopandas as gdp
from bson.json_util import dumps

import src.conversion_functions as cf 
import src.geofunctions as gf

load_dotenv()

client_id = os.getenv('Client_Id')
client_secret = os.getenv('Client_Secret')

url_query = 'https://api.foursquare.com/v2/venues/search'

lista = ['Vegan', 'Start Up', 'Veterinary', 'Bar', 'Starbucks']

df_full_ny = []
for i in lista:
    df_ny = cf.todo('https://api.foursquare.com/v2/venues/search','40.75673, -73.98996', i, client_id, client_secret)
    df_full_ny.append(df_ny)
df_NewYork = pd.concat(df_full_ny)

df_full_mad = []
for i in lista:
    df_mad = cf.todo('https://api.foursquare.com/v2/venues/search','40.50222, -3.67097', i, client_id, client_secret)
    df_full_mad.append(df_mad)
df_Mad = pd.concat(df_full_mad)


df_full_bcn = []
for i in lista:
    df_bcn = cf.todo('https://api.foursquare.com/v2/venues/search','41.40080, 2.19763', i, client_id, client_secret)
    df_full_bcn.append(df_bcn)
df_Bcn = pd.concat(df_full_bcn)

df_NewYork.to_csv('newyork_data.csv')
df_Mad.to_csv('mad_data.csv')
df_Bcn.to_csv('bcn_data.csv')


#Mongo Cosas

df = pd.read_csv('newyork_data.csv', index_col = 0)
df2 = pd.read_csv('mad_data.csv', index_col = 0)
df3 = pd.read_csv('bcn_data.csv', index_col = 0)

coord_ny = [-73.98996, 40.75673]
coord_mad = [2.19763, 41.40080]
coord_bcn = [-3.67097, 40.50222]

lista1 = [df,df2,df3]
lista2 = ['ny', 'mad','bcn']

for i,j in zip(lista1,lista2):
    gf.funcionquefunciona(i,j)


client = MongoClient("localhost:27017")
db = client.get_database("GeoProject3")

m = db.get_collection("mad")
b = db.get_collection("bcn")
ny = db.get_collection('ny')

ny_ = gf.todo2 ([-73.98996, 40.75673], ny)
bcn_ = gf.todo2([-3.67097, 40.50222], b)
mad_ = gf.todo2([2.19763, 41.40080], m)

ny_agregado = gf.agrega(ny_)
mad_agregado = gf.agrega(mad_)
bcn_agregado = gf.agrega(bcn_)


ny_acortado = ny_agregado[(ny_agregado['tipo'] == 'Vegetarian / Vegan Restaurant') | (ny_agregado['tipo'] == 'Café')
             | (ny_agregado['tipo'] == 'Tech Startup') | (ny_agregado['tipo'] == 'Bar')]

bcn_acortado = bcn_agregado[(bcn_agregado['tipo'] == 'Vegetarian / Vegan Restaurant') | (bcn_agregado['tipo'] == 'Café')
             | (bcn_agregado['tipo'] == 'Tech Startup') | (bcn_agregado['tipo'] == 'Food & Drink Shop')]


ny_acortado.to_csv('valores_ny.csv')
bcn_acortado.to_csv('valores_bcn.csv')
