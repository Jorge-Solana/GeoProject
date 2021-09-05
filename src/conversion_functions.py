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
    Esta función bucea por el diccionario que le damos en base a un mapa (ruta) que también se le da.
    Dentro de el diccionario irá a donde el mapa le indique.
    Recibe : diccionario y mapa ('hoja de ruta')
    Devuelve: lo espcificado dentro del diccionario pr el mapa
    '''
    from functools import reduce
    import operator
    return reduce(operator.getitem,mapa,diccionario)


def getAPI(url_query, coordenadas, query): #coordenadas en string, latitud y longitud (en ese orden)
    '''
    Esta función llama a la API en base a unas coordenadas y a una query que le demos (restaurantes, gimansios, etc.) 
    y nos devuelve un json.
    Recibe : url de la API, coordenadas (en formato string), query (qué queremos que nos busque)
    Devuelve: json en base a los parámetros establecidos
    '''
    parametros = {
    "client_id": client_id,
    "client_secret": client_secret,
    "v": "20180323",
    "ll": f'{coordenadas}',
    "query": f"{query}",
    "limit": 200   
}
    resp = requests.get(url_query, params=parametros).json()['response']['venues']
    
    return resp


def limpiezaresp(json):
    '''
    Esta función limpia la respuesta json que nos devuelve la llamada a la API.
    Dentro del for loop llama a la función getFromDict con los mapas(rutas), establecidos en esta función,
    y coge lo que le indicamos dentro de esa ruta y lo coloca ordenado según lo que le indiquemos (nombre, logitud, etc).
    Estas itercaiones las coloca en un json nuevo (jason), al que se va apendando cada iteración. Por último
    nos devuelve ese jsno en forma de data frame.
    Recibe: json
    Devuelve: dataframe
    
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
    return pd.DataFrame(jason)


def todo(url_query, coordenadas, query):
    '''
    Esta función resume la función de la llamada a la API y la limpieza del json, llama a las dos.
    Recibe: la url de la API, las coordenadas de la localización a estudiar y la query que queremos que nos devuelva la API
    Devuelve: el json limpio con la información justa que queremos.
    '''
    api = getAPI(url_query, coordenadas, query)
    return limpiezaresp(api)

