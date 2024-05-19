import requests
import os
import json
import pandas as pd
from datetime import datetime

from notionDAO import read_data, create_page, update_page, delete_page, listacompradata



def update_lista_compra(api_secret:str, db_comidas:str, db_lista:str):

    data_comidas = read_data(api_secret, db_comidas)
    lista_compra = list()
    for page in data_comidas:
        if not page['properties']['Comprado']['checkbox']:
            for ing in page['properties']['Ingredientes']['multi_select']:
                new_ing = ing['name']
                if new_ing not in lista_compra:
                    print(new_ing)
                    lista_compra.append(new_ing)    
                    create_page(
                        api_secret=api_secret,
                        db_id=db_lista,
                        data=listacompradata(new_ing)
                        )
                
    return                
