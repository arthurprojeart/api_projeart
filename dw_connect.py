import pyodbc
import pandas as pd
import os
from dotenv import load_dotenv  
import json
load_dotenv()

def connect_projeart():
    server = os.getenv('SERVER')
    user = os.getenv('USER_DW')
    password = os.getenv('PASSWORD')
    db = os.getenv('DBPROJEART')
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+db+';UID='+user+';PWD='+ password, TrustServerCertificate='Yes')
    cursor = cnxn.cursor()
    return cursor

def connect_dw():
    server = os.getenv('SERVER')
    user = os.getenv('USER_DW')
    password = os.getenv('PASSWORD')
    db = os.getenv('DBDW')
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+db+';UID='+user+';PWD='+ password, TrustServerCertificate='Yes')
    cursor = cnxn.cursor()
    return cursor
import numpy as np
def query_obras():
    cursor = connect_dw()
    cursor.execute(f'''
    Select * From DW_Obras

------------------------------------------------------------------''')
    rows_obras = cursor.fetchall()
    ObraID = []
    Obra = []
    
    for i in range(len(rows_obras)):
        ObraID.append(rows_obras[i][0])
        Obra.append(rows_obras[i][1])
    df_obras = pd.DataFrame(ObraID, columns=['ObraID'])   
    df_obras['Obra'] = Obra
    obras_json = df_obras.to_json(orient="records", force_ascii=False)
    #Obra = cursor.Obra()
    #df_obras = pd.DataFrame(rows)
    
    return obras_json

def query_trechos(obra_id):
    cursor = connect_dw()
    cursor.execute(f'''
    Select * From DW_ObrasTrechos where ObraID like '%{obra_id}%'

------------------------------------------------------------------''')
    rows_obras = cursor.fetchall()
    ObraID = []
    Obra = []
    
    for i in range(len(rows_obras)):
        ObraID.append(rows_obras[i][6])
        Obra.append(rows_obras[i][7])
    df_obras = pd.DataFrame(ObraID, columns=['TrechoID'])   
    df_obras['Trecho'] = Obra
    df_obras = df_obras.to_json(orient="records", force_ascii=False)
    #Obra = cursor.Obra()
    #df_obras = pd.DataFrame(rows)
    
    return df_obras

def query_get_peca(ordem_ou_nome):
    #if type(ordem_ou_nome) is int:
    ordem_ou_nome = str(ordem_ou_nome)
    cursor = connect_projeart()
    cursor.execute(f'''
        SELECT 
	OrdemDeFabricacao = Lot.CdLot
,	NomePeca = ObjPrd.NmObj
,	Obra = LotObr.NmLot
,	IdObra = LotObr.CdLot
,	Trecho = Tre.TtOpl
,	IdTrecho = Tre.CdLot
,	Marca = Mar.TtOpo
,	Desenho = OplDes.TtOpl
,	PesoUnitario = Uap.QtUapLiq
,	QuantidadeProduzida = Lot.QtLotPrdUap
FROM TbLot Lot 
left join	TbObj Obj on Obj.CdObj = Lot.CdObjPrd 
join TbOpl UltProc (NOLOCK) on  UltProc.CdLot = Lot.CdLot
							and UltProc.CdCrc = 299 -- Ultimo Processo
JOIN TbUap Uap (NOLOCK) on Uap.CdUap = Lot.CdUap
left join TbPex Pex (NOLOCK) on  Pex.CdPex = Lot.CdPex
JOIN TbPxo Pxo on Pxo.CdPxo = Pex.CdPxoPri
  JOIN TbPxa Pxa on Pxa.CdPxo = Pxo.CdPxo
JOIN TbLot LotAtv on LotAtv.CdLot = Pxa.CdLotAtv
join      TbObj ObjPrd     on  ObjPrd.CdObj = Lot.CdObjPrd
LEFT JOIN TbOpl OplDes (NOLOCK) on OplDes.CdLot = Lot.CdLot 
						and OplDes.CdCrc = 274 --Desenho
LEFT JOIN TbOpl Obt (NOLOCK) on  Obt.CdLot = Lot.CdLot
							AND Obt.CdCrc = 261 -- 1. Obra/Trecho
  LEFT JOIN TbOpl Obr (NOLOCK) on  Obr.CdLot = CONVERT(Int, SUBSTRING(Obt.NrOplRef, PATINDEX('%'+CHAR(160)+'%', Obt.NrOplRef) + 1, LEN(Obt.NrOplRef)))
							AND Obr.CdCrc = 258 -- OBRA
  LEFT JOIN TbLot LotObr (NOLOCK) on LotObr.CdLot = CONVERT(Int, SUBSTRING(Obr.NrOplRef, PATINDEX('%'+CHAR(160)+'%', Obr.NrOplRef) + 1, LEN(Obr.NrOplRef)))

LEFT JOIN TbOpl Tre (NOLOCK) on  Tre.CdLot = CONVERT(Int, SUBSTRING(Obt.NrOplRef, PATINDEX('%'+CHAR(160)+'%', Obt.NrOplRef) + 1, LEN(Obt.NrOplRef)))
							AND Tre.CdCrc = 260 -- TRECHO


  LEFT JOIN TbOpo Mar (NOLOCK) on  Mar.CdObj = Obj.CdObj
							AND Mar.CdCrc = 249 -- Marca

WHERE
	Lot.TpLotSta = 1 -- Apenas em Aberto
	And Lot.CdObj = 40766 --OF - PROJEART
    And (Lot.CdLot = {ordem_ou_nome} or ObjPrd.NmObj like '%{ordem_ou_nome}%')

--and Obj.CdObj003 = 39385 -- Apenas COMPONENTES

GROUP BY
	Lot.CdLot
,	Lot.QtLotUap
,	Lot.QtLot
,	Uap.QtUapLiq
,	Pex.CdPxoPri
,	LotAtv.CdLot
,	Lot.QtLotPrdUap
,	ObjPrd.NmObj
,	OplDes.TtOpl
,	LotObr.NmLot
,	LotObr.CdLot
,	Mar.TtOpo
,	ObjPrd.NmObj
,	Tre.TtOpl
,	Tre.CdLot

        ------------------------------------------------------------------''')
    
    rows = cursor.fetchall()
    rows = list(rows[0]) 
    df_peca = pd.DataFrame(rows, index=['OrdemDeFabricacao', 'NomePeca','Obra','IdObra','Trecho','IdTrecho','Marca','Desenho','PesoUnitario','QuantidadeProduzida'])
    df_peca = df_peca.transpose()
    peca_json = df_peca.to_json(orient="records", force_ascii=False)

    return peca_json
#print(query_get_peca('D7-3-01'))
def query_post_romaneio(romaneio):
    return



