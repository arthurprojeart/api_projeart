import pyodbc
import pandas as pd
import os
from dotenv import load_dotenv  
load_dotenv()

def connect_projeart():
    server = os.getenv('SERVER')
    user = os.getenv('USER_DW')
    password = os.getenv('PASSWORD')
    db = os.getenv('DBPROJEART')
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+db+';UID='+user+';PWD='+ password, TrustServerCertificate='Yes')
    cursor = cnxn.cursor()
    return cursor

def connect_dw():
    server = os.getenv('SERVER')
    user = os.getenv('USER_DW')
    password = os.getenv('PASSWORD')
    db = os.getenv('DBDW')
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+db+';UID='+user+';PWD='+ password, TrustServerCertificate='Yes')
    cursor = cnxn.cursor()
    return cursor

def query_obras():
    cursor = connect_dw()
    cursor.execute(f'''
    Select * From DW_Obras

------------------------------------------------------------------''')
    df_obras = cursor.fetchall()
    #Obra = cursor.Obra()
    #df_obras = pd.DataFrame(rows)
    
    return df_obras

print(query_obras())



