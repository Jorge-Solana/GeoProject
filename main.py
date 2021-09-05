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

url_query = 'https://api.foursquare.com/v2/venues/search'

lista = ['Vegan', 'Start Up', 'Veterinary', 'Bar', 'Starbucks']

df_full_ny = []
for i in lista:
    df_ny = cf.todo('https://api.foursquare.com/v2/venues/search','40.75673, -73.98996', i)
    df_full_ny.append(df_ny)
df_NewYork = pd.concat(df_full_ny)

df_full_mad = []
for i in lista:
    df_mad = cf.todo('https://api.foursquare.com/v2/venues/search','40.50222, -3.67097', i)
    df_full_mad.append(df_mad)
df_Mad = pd.concat(df_full_mad)


df_full_bcn = []
for i in lista:
    df_bcn = cf.todo('https://api.foursquare.com/v2/venues/search','41.40080, 2.19763', i)
    df_full_bcn.append(df_bcn)
df_Bcn = pd.concat(df_full_bcn)

df_NewYork.to_csv('newyork_data.csv')
df_Mad.to_csv('mad_data.csv')
df_Bcn.to_csv('bcn_data.csv')


#Mongo Cosas

coord_ny = [-73.98996, 40.75673]
coord_mad = [2.19763, 41.40080]
coord_bcn = [-3.67097, 40.50222]

lista1 = [df,df2,df3]
lista2 = ['ny', 'mad','bcn']

for i,j in zip(lista1,lista2):
    gf.funcionquefunciona(i,j)

from pymongo import MongoClient
client = MongoClient("localhost:27017")
db = client.get_database("GeoProject")

m = db.get_collection("mad")
b = db.get_collection("bcn")
ny = db.get_collection('ny')

query = [{'$geoNear': {'near':[-73.98996, 40.75673],
                      'distanceField' : 'distance',
                       'maxDistance': 6000,
                       'distanceMultiplier': 6371,
                       'spherical': True}}]
geoloc_ny = ny.aggregate(query)
ny_response_json = json.loads(dumps(geoloc_ny))

query2 =[{'$geoNear': {'near':[2.19763, 41.40080],
                      'distanceField' : 'distance',
                       'maxDistance': 6000,
                       'distanceMultiplier': 6371,
                       'spherical': True}}]
geoloc_mad = m.aggregate(query2)
mad_response_json = json.loads(dumps(geoloc_mad))

query3 =[{'$geoNear': {'near':[-3.67097, 40.50222],
                      'distanceField' : 'distance',
                       'maxDistance': 6000,
                       'distanceMultiplier': 6371,
                       'spherical': True}}]
geoloc_bcn = b.aggregate(query3)
bcn_response_json = json.loads(dumps(geoloc_bcn))

ny = gf.toDataFrame(json_normalize(ny_response_json))
mad = gf.toDataFrame(json_normalize(mad_response_json))
bcn = gf.toDataFrame(json_normalize(bcn_response_json))


