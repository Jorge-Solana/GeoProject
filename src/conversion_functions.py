import requests
import json
from dotenv import load_dotenv
import os
import pandas as pd
from pymongo import MongoClient
from pandas import json_normalize
from pymongo import MongoClient,GEOSPHERE
import shapely.geometry
import geopandas



def getFromDict(diccionario, mapa):
    '''
    Esta función bucea por el diccionario según le indiquemos con el mapa.
    Args: 
        diccionario (dict)
        mapa ()
    Returns: 
        un chorizamen 
    '''
    from functools import reduce
    import operator
    return reduce(operator.getitem,mapa,diccionario)


def getAPI(url_query, coordenadas, query, client_id, client_secret): 
    '''
    Esta función llama a la API.
    
    Args: 
        url_query (url)
        coordenadas (str)
        query (str)
    Returns: 
        resp (json)
    '''
    parametros = {
    "client_id": client_id,
    "client_secret": client_secret,
    "v": "20180323",
    "ll": f'{coordenadas}',
    "query": f"{query}",
    "limit": 200   
}
    # a continuación en base a los parámetros establecidos hacemos la llamada conviertondola en un json
    # y especificando que nos devuelva lo que hay dentro de 'venues' que está a su vez dentro de 'response'
    
    resp = requests.get(url_query, params=parametros).json()['response']['venues']
    
    return resp


def limpiezaresp(json):
    '''
    Esta función limpia la respuesta json que nos devuelve la llamada a la API convirtiendola en un data frame.
    
    Args: 
        json (list[dict]) 

    Returns: 
        pd.DataFrame: data frame con 6 columnas
    
    '''
    mapa_nombre = ['name']
    mapa_latitud = ['location','lat']
    mapa_longitud = ['location', 'lng']
    mapa_ciudad = ['location','city']
    mapa_distancia = ['location','distance']
    
    
    jason = []
    
    for dic in json:
        try:
            diccio= {}
            diccio['nombre']= getFromDict(dic,mapa_nombre)
            diccio['latitud']= getFromDict(dic,mapa_latitud)
            diccio['longitud']= getFromDict(dic,mapa_longitud)
            diccio['ciudad']= getFromDict(dic,mapa_ciudad)
            diccio['distancia'] = getFromDict(dic,mapa_distancia)
            jason.append(diccio)
        except:
            pass
    
    df = pd.DataFrame(jason)
    
    # aqui hacemos un for denrto de otro for para bucear dentro de la respuesta del json, ya que con el mapa no podemos
    # sacaremos el tipo de de cada una de nuestras categorías y esto lo apendamos a una lista la cual luego la convertimos
    # en una columna nueva de nuestro data frame
    tipo = []
    for i in json:
        for z in i["categories"]:
            tipo.append(z["name"])
    tipo = pd.Series(tipo) #si no se convierte en una serie de pandas no se une correctamente al dataframe final
    
    df['tipo'] = tipo
    
    return df


def todo(url_query, coordenadas, query, client_id, client_secret):
    '''
    Llama a la API y y limpia la respuesta.
    Args: 
        url_query (url)
        coordenadas (str)
        query (str)
    Returns: 
        pd.DataFrame
    '''
    api = getAPI(url_query, coordenadas, query, client_id, client_secret) 
    return limpiezaresp(api) 

