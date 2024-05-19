# Funciones externas
import os
from dotenv import load_dotenv

# Funciones internas
from functions import update_lista_compra

# GLOBAL VARIABLES
load_dotenv("env")
NOTION_SECRET = os.getenv('notion_secret')
CAL_ID = os.getenv('calendario_id')
LDC_ID = os.getenv('lista_de_compra_id')


### Start main
def main():
    update_lista_compra(
        api_secret=NOTION_SECRET,
        db_comidas=CAL_ID,
        db_lista=LDC_ID
    )

### End main


if __name__ == '__main__':
    main()