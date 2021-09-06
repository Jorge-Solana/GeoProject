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



def funcionquefunciona(df, ciudad):
    '''
    Esta función coge un dataframe y lo convierte en base de datos en Mongo db.
    Args:
        df (pd.DataFrame)
        ciudad (str)
    Returns: 
        mensaje Buenísima (str): mensaje que nos indica que se han creado con éxito las colecciones dentro de la base de datos   
    '''
    
    # a continuación transformamos el dataframe que entra en un geodataframe y generamos la geometría para luego hacer las geoqueries
    
    gdf = gdp.GeoDataFrame(df, geometry= gdp.points_from_xy(df.longitud, df.latitud ))
    print(gdf.columns)
    gdf.columns=['nombre', 'latitud','longitud','ciudad','distancia','tipo','loc2' ]
    
    gdf['loc2']= gdf['loc2'].apply(lambda x:shapely.geometry.mapping(x))
    
    client = MongoClient()
    db = client.GeoProject3
    collection = db.create_collection(name = f'{ciudad}')
    collection = db[f'{ciudad}']
    collection.create_index([("loc2", "2dsphere")])
    data = gdf.to_dict(orient='records')
    collection.insert_many(data)
    
    return 'Buenisima'


def geoquery(coordenadas, coleccion): #las coordenadas en formato lista (long y lat)
    '''
    Esta función nos la query de geoNear a la colección de Mongo indicada.
    Args: 
        coordenadas (list)
        coleccion (pymongo.collection.Collection)
    Returns: 
        response_json (json)
    '''
    query = [{'$geoNear': {'near':coordenadas,
                      'distanceField' : 'distance',
                       'maxDistance': 6000,
                       'distanceMultiplier': 6371,
                       'spherical': True}}]
    
    
    # aquí vamos a agregar la query especificada antes a una colección en concreto y la respuesta la convertiremos en un json
    col = coleccion
    geoloc = col.aggregate(query)
    response_json = json.loads(dumps(geoloc))
    
    return response_json




def toDataFrame(df):
    '''
    Esta función recibe un dataframe y nos lo limpia.
    Args: 
        df (pd.DataFrame)
    Returns: 
        df (pd.DataFrame): filtrado por la distancia indicada
    '''
    
    df = df[['nombre', 'ciudad', 'distancia']] # estas son las 3 columnas que nos interesan en nuestro dataframe
    df = df[df['distancia'] < 6000] # especificamos la distancia máxima a la que tiene que filtrar
    return df


def todo2(coordenadas, coleccion):
    '''
    Hace la geoquery y convierte la respuesta en un dataframe.
    Args: 
        coordenadas (list)
        coleccion (pymongo.collection.Collection)
    Returns: 
        df (pd.DataFrame)
    
    '''
    geo = geoquery(coordenadas, coleccion)
    return toDataFrame (json_normalize(geo))


def agrega(df):
    '''
    Hace un groupby y resetea el index del dataframe.
    Args: 
        df (pd.DataFrame)
    Returns: 
        df_agregado (pd.DataFrame): la columna 'tipo' tiene valores únicos y la 'distancia' es la media de los valores de 'tipo'
    
    '''
    df_agregado = df.groupby('tipo').agg({'distancia': 'mean'})
    df_agregado.reset_index(inplace = True)
    return df_agregado