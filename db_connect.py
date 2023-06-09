import pyodbc
import pandas as pd
import os
from dotenv import load_dotenv  
import json
load_dotenv()


def connect_custom():
    server = os.getenv('SERVER')
    user = os.getenv('USER_DW')
    password = os.getenv('PASSWORD')
    db = os.getenv('DBCUSTOM')
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+db+';UID='+user+';PWD='+ password, TrustServerCertificate='Yes')
    cursor = cnxn.cursor()
    return cursor

def query_delete_pecas(id_romaneio):
    cursor = connect_custom()
    cursor.execute(f'''
    DELETE FROM TbPecasRomaneio WHERE ID_TbRomaneio = {id_romaneio}

------------------------------------------------------------------''')
    
    return True

def query_delete_romaneio(id_romaneio):
    cursor = connect_custom()
    cursor.execute(f'''
    DELETE FROM TbRomaneio WHERE ID_Romaneio = {id_romaneio}

------------------------------------------------------------------''')
    
    return True

def query_insert_peca(id_peca):
    cursor = connect_custom()
    cursor.execute(f'''
    DELETE FROM TbRomaneio WHERE ID_Romaneio = {id_peca}

------------------------------------------------------------------''')
    
    return True