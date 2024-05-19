import requests
from dotenv import load_dotenv
import os
import json
import pandas as pd
from datetime import datetime



# CRUD functions for Notion API

## CREATE
def create_page(api_secret:str, db_id: str, data:dict):
    create_endpoint = "https://api.notion.com/v1/pages"
    headers = {
    "Authorization" : "Bearer " + api_secret,
    "Content-Type" : "application/json",
    "Notion-Version" : "2022-06-28"
    }
    payload = {
        "parent" : {
            "database_id" : db_id
        },
        "properties" : data
    }

    result = requests.post(create_endpoint, headers = headers, json = payload)
    print(result.status_code)
    return result

## READ
def read_data(api_secret:str, db_id:str, dump_json:bool = False, num_pages:int=None):
    headers = {
    "Authorization" : "Bearer " + api_secret,
    "Content-Type" : "application/json",
    "Notion-Version" : "2022-06-28"
    }
    endpoint_url =  f'https://api.notion.com/v1/databases/{db_id}/query'
    get_all = num_pages is None
    page_size = 100 if get_all else num_pages
    payload = {"page_size" : page_size}

    response = requests.post(endpoint_url, json = payload, headers=headers)      
    data = response.json()
    
    try:
        results = data['results']
        
        while data['has_more'] and get_all:
            payload = {
                'page_size' : page_size,
                'start_cursor' : data['next_cursor']
            }
            response = requests.post(endpoint_url, json = payload, headers=headers)
            data = response.json()
            results.extend(data['results'])

        if dump_json:
            with open('dump.json', 'w') as f:
                json.dump(results, f, indent = 4)

        return results
    
    except:
        print("Ha habido un error en la conexión")
        print(data)
        return data        

## UPDATE
def update_page(api_secret:str, page_id: str, data:dict):
    create_endpoint = f"https://api.notion.com/v1/pages/{page_id}"
    headers = {
    "Authorization" : "Bearer " + api_secret,
    "Content-Type" : "application/json",
    "Notion-Version" : "2022-06-28"
    }
    payload = {
        "properties" : data
    }

    result = requests.patch(create_endpoint, headers = headers, json = payload)
    print(result.status_code)
    return result

## DELETE
def delete_page(api_secret:str, page_id: str):
    create_endpoint = f"https://api.notion.com/v1/pages/{page_id}"
    headers = {
    "Authorization" : "Bearer " + api_secret,
    "Content-Type" : "application/json",
    "Notion-Version" : "2022-06-28"
    }
    payload = {
        "archived" : True
    }

    result = requests.patch(create_endpoint, headers = headers, json = payload)
    print(result.status_code)
    return result


#### 

# Data structures

## Lista de la compra
def listacompradata(ingrediente:str, check:str = "false"):
    dct = {
        "ingrediente" : ingrediente,
        "check" : check
    }
    page = """
        {
            "Comprado": {
                "id": "rGpQ",
                "type": "checkbox",
                "checkbox": %(check)s
            },
            "Ingrediente": {
                "id": "title",
                "type": "title",
                "title": [
                    {
                        "type": "text",
                        "text": {
                            "content": "%(ingrediente)s",
                            "link": null
                        },
                        "annotations": {
                            "bold": false,
                            "italic": false,
                            "strikethrough": false,
                            "underline": false,
                            "code": false,
                            "color": "default"
                        },
                        "plain_text": "%(ingrediente)s",
                        "href": null
                    }
                ]
            }
        }
    """ % dct
    
    return json.loads(page)