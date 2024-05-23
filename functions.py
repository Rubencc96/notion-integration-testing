import requests
import os
import json
import pandas as pd
from datetime import datetime

from notionDAO import read_data, create_page, update_page, delete_page, listacompradata


def _deletePreviousItems(api_secret:str, db_lista:str):
     compra_data = read_data(api_secret, db_lista)
     for row in compra_data:
        if row['properties']['Comprado']['checkbox']:
        
            delete_page(api_secret, row['id'])
          

def deletePreviousComidas(api_secret:str, db_comidas:str):
    comidas_data = read_data(api_secret, db_comidas)
    for page in comidas_data:
        date_obj = page['properties']['Día']['date']
        if not date_obj:
            delete_page(api_secret, page['id'])
            continue

        date_comida=datetime.strptime(date_obj['start'], "%Y-%m-%d")
        if datetime.now().date() > date_comida.date():
            delete_page(api_secret, page['id'])


def updateListaCompra(api_secret:str, db_comidas:str, db_lista:str):
    _deletePreviousItems(api_secret, db_lista)
    data_comidas = read_data(api_secret, db_comidas)
    lista_compra = list()
    for page in data_comidas:
            if page['properties']['Ingredientes']['rollup']['array']:
        # rezaré porque el 0 del array sea siempre 0, en principio debería interarse pero 
        # las relaciones son únicas
                for ing in page['properties']['Ingredientes']['rollup']['array'][0]['multi_select']:
        
                    new_ing = ing['name']
                    if new_ing not in lista_compra:
                        # print(new_ing)
                        lista_compra.append(new_ing)    
                        # create_page(
                        #     api_secret=api_secret,
                        #     db_id=db_lista,
                        #     data=listacompradata(new_ing)
                        #     )
            for extra_ing in page['properties']['Ingredientes adicionales']['multi_select']:
                 new_ing = extra_ing['name']
                 lista_compra.append(new_ing)

    lista_compra_unique = list(set(lista_compra))
    for item in lista_compra_unique:
         create_page(
              api_secret=api_secret,
              db_id=db_lista,
              data=listacompradata(item)
         )
                
    return         
