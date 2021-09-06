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



def funcionquefunciona (df,ciudad):
    '''
    Esta función va a recibir un dataframe y una ciudad y lo que va a hacer es, transformar ese dataframe en un
    geodataframe generando las coordenadas como las lee mongo db y creando una nueva columna con las mismas (por cada
    uno de los estableciemientos en nuestro dataframe original). Seguidamente, se conecta con Mongo db y nos crea 
    la base de datos con sus coleccions (la ciudad que le pasamos) y genera un index de tipo 2dspehere para cada valor
    de la nueva columna de coordenadas generada antes, para poder hacer posteriormente las geoqueries.
    Recibe: un dataframe y una ciudad
    Devuelve: un mensaje que nos indica que la base de datos con las colecciones y los index han sido creados con éxito
    
    '''
    gdf = gdp.GeoDataFrame(df, geometry= gdp.points_from_xy(df.lng, df.lat ))
    print(gdf.columns)
    gdf.columns=['nombre', 'lat','lng','ciudad','distancia','loc','loc2' ]
    
    gdf['loc2']= gdf['loc2'].apply(lambda x:shapely.geometry.mapping(x))
    
    client = MongoClient()
    db = client.GeoProject
    collection = db.create_collection(name = f'{ciudad}')
    collection = db[f'{ciudad}']
    collection.create_index([("loc2", "2dsphere")])
    data = gdf.to_dict(orient='records')
    collection.insert_many(data)
    
    return 'Buenisima'


def geoquery(coordenadas, coleccion): #las coordenadas en formato lista (long y lat)
    '''
    Esta función, a partir de unas coordenadas y de una colección que tenemos creada en Mongo db, nos devuelve un json. 
    Esto lo hace a través de la query geoNear, donde esecificamos los criterios que debe seguir la misma. Después 
    llamamos a la colección y agregamos la query a la misma y a la respuesta que nos da le aplicamos un dumps y nos 
    devuelve un json con los ruquerimientos especificados.
    Recibe: coordenadas (formato lista) y colección de Mongo db (previamente hecha la conexión)
    Devuelve: json
    '''
    query = [{'$geoNear': {'near':coordenadas,
                      'distanceField' : 'distance',
                       'maxDistance': 6000,
                       'distanceMultiplier': 6371,
                       'spherical': True}}]
    
    col = coleccion
    geoloc = col.aggregate(query)
    response_json = json.loads(dumps(geoloc))
    
    return response_json




def toDataFrame (df):
    '''
    Esta función recibe un dataframe y nos lo limpia y filtra por la distancia que le especifiquemos.
    Recibe: dataframe
    Devuelve: dataframe filtrado 
    '''
    
    df = df[['nombre', 'ciudad', 'distancia']]
    df = df[df['distancia'] < 6000]
    return df


def todo2 (coordenadas, coleccion):
    '''
    Esta función une la función de geoquery y la función de toDataFrame y me hace las dos en una.
    Recibe: coordenadas (en formato lista) y una colección de Mongo db (previamente conectada)
    Return: un dataframe filtrado por las condiciones establecidas en la función toDataFrame
    
    '''
    geo = geoquery(coordenadas, coleccion)
    return toDataFrame (json_normalize(geo))


def agrega (df):
    '''
    Esta función me genera un dataframe nuevo a partir de otro, haciendo un grouby por tipo y haciendo una media de la
    distancia de todos los valores que tienen ese mismo tipo en nuestro dataframe.
    Recibe: dataframe donde en 'tipo' hay valores reepetidos
    Return: dataframe con valores en 'tipo' únicos y otra columna de distancia que es la media de todos los repetidos
    
    '''
    df_agregado = df.groupby('tipo').agg({'distancia': 'mean'})
    df_agregado.reset_index(inplace = True)
    return df_agregado