# Proyecto de geolocalización de una empresa

## Objetivos

En este proyecto se pretende econtrar la localización ótima, en base a unos criteros que después se explicarán, de una empresa.

## Metodología

Para la realización de este proyecto se han seguuido una serie de pasos:
- El primero ha sido, en base a todo lo que sabíamos de la empresa, en cuanto a necesidades y gustos, generar una prioridades. (Se puede decir que estas prioridades podrían haber sido sacadas después de haber hecho una encuesta a todos los trabajadores para saber qué tiene más peso). En nuestro caso de estudio, los criterios elegidos son (por orden de prioridad) : Tener una startup grande cerca, tener restaurantes veganos cerca (ya que el CEO es vegano, este criterio tiene mucho peso), tener Starbucks cerca, que haya algún veterinario cerca (ya que el perro Dobby es muy querido por todos los integrnates de la empresa) y por último la proximidad a un bar.

- Una vez escogidos estos criterios, se han tenido que escoger entre 3 ciudades del mundo, en nuestro caso Nueva York, Madrid y Barcelona. Concreteamente dentro de estas ciudades, se han buscado lugares donde la empresa no se encontrase de manera solitaria.

- Posteriormente, se han empezado a hacer llamadas a la API, teniendo en cuenta los criterios escogidos en el paso 1. La API que se ha usado para estas llamadas es [Foursquare](https://foursquare.com/) .

- Con esas llamadas a la API nos hemos generado 3 data frames diferntes, uno para cada ciudad de estudio (Madrid, Barcelona y Nueva York). Estos data frames se han exportado en formato .csv para posteriormente cargarlos en Mongo db y poder hacer las geoqueries correspondientes.

- Una vez cargados en Mongo db, empezamos a hacer las geoqueries, tan solo se realizará una (geoNear), la cual la utilizaremos para coger todos las localizaciones de nuestros criterios de cada ciudad a una distancia máximas que nosotros les indiquemos. (Como se comenta dentro del código, al final utilizaremos la distancia aportada por el json en vez del geoNear, dentro se explica el por qué de esta decisión). 

- Finalmente, teniedo unso data frames limpios con nuestra información necesaria por cada ciudad, se ha realizado una ponderación en base a cuál de nuestros criterios tiene mayor prioridad. Estos cálculos se han realizado de la siguiente manera:

    - Primero se ha calculado la media de cada uno de los parámetros a las coordenadas de nuestra localización.

    - Con ese valor medio se han hecho las ponderaciones correspondientes, las cuales son las que siguen:

        - Start Up x 1.0
        - Restaurante vegano x 0.85
        - Starbucks x 0.75
        - Veterinario x 0.5
        - Bar x 0.25
    
    - Teniendo las ponderaciones de cada parámetro de cada ciudad, queremos reducir estos 5 valores en tan solo 1 para tener una estimación de lo buena o mala que es esa ciudad para situar la empresa, para ello se ha realizado un sumatorio de todos los valore y luego se ha normalizado sobre 10, para ser más claro. El número menor será el mejor valor.

## Conclusiones

Finalmente, después de realizar la ponderación y la normalización, vemos que la mejor ciudad para localizar la empresa es Nueva York ya que es la ciudad que tiene las prioridades de la empresa más cerca que las otras ciudades del estudio, además, es la única que tiene un centro veterinario dentro de un radio menor de 6 kilómetros.

## Librerías usadas

- [Pandas](https://pandas.pydata.org/)

- [Geopandas](https://geopandas.org/)

- [Json](https://www.json.org/json-en.html)

- [Shapely-geometry](https://shapely.readthedocs.io/en/stable/manual.html)

- [Dotenv](https://pypi.org/project/python-dotenv/)

- [Os](https://docs.python.org/3/library/os.html)

- [Requests](https://docs.python-requests.org/en/master/)

- [Operator](https://docs.python.org/3/library/operator.html)

