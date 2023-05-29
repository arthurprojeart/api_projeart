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

    if type(ordem_ou_nome) is int:
        ordem = ordem_ou_nome
        nome = '@@@@@@@@@@@@@'
    
    else:
        nome = ordem_ou_nome
        ordem = ordem_ou_nome

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
,   QuantidadeTotal = Lot.QtLotUap

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
	--Lot.TpLotSta = 1 -- Apenas em Aberto
	--And 
    Lot.CdObj = 40766 --OF - PROJEART
    And (Lot.CdLot  like '%{ordem}%' or ObjPrd.NmObj like '%{nome}%')

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
    if len(rows) > 0:
        lista_geral = []
        for i in range(len(rows)):
            lista_geral.append(list(rows[i]))

        df_peca = pd.DataFrame(lista_geral, columns=['Ordem_Fabricacao', 'Nome_Peca','Nome_Obra','ID_Obra','Nome_Trecho','ID_Trecho','Marca','Desenho','Peso_Unitario','Quantidade_Produzida', 'Quantidade_Projeto'])
        #df_peca = pd.DataFrame(lista_geral)
        #df_peca = df_peca.transpose()\
        lista_dict = []
        for i in range(len(df_peca)):
            lista_dict.append(dict(df_peca.iloc[i]))
        # print(lista_dict)
        # peca_json = df_peca.to_json(orient="records", force_ascii=False)
    else:
        lista_dict = 0
    return lista_dict

def query_get_ordem(Ordem_Fabricacao):

    if type(Ordem_Fabricacao) is int:
        ordem_certa = Ordem_Fabricacao
    else:
        ordem_certa = int(Ordem_Fabricacao)
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
,   QuantidadeTotal = Lot.QtLotUap
,   ID_Romaneio = 1
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
	--Lot.TpLotSta = 1 -- Apenas em Aberto
	--And 
    Lot.CdObj = 40766 --OF - PROJEART
    And Lot.CdLot = {ordem_certa}

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
    # print(rows)
    rows = list(rows[0]) 
    df_peca = pd.DataFrame(rows, index=['Ordem_Fabricacao', 'Nome_Peca','Nome_Obra','ID_Obra','Nome_Trecho','ID_Trecho','Marca','Desenho','Peso_Unitario','Quantidade_Produzida', 'Quantidade_Projeto','ID_TbRomaneio'])
    #df_peca.iloc[7] = pd.to_numeric(df_peca.iloc[7])

    if df_peca.iloc[6][0] is None:
        df_peca.iloc[6][0] = df_peca.iloc[1][0].split(' ')[0]

    df_peca.iloc[8] = pd.to_numeric(df_peca.iloc[8])
    df_peca.iloc[9] = pd.to_numeric(df_peca.iloc[9])
    df_peca.iloc[7] = '1'
    #teste = list(df_peca[0])
    peca_dict = df_peca.to_dict()
    peca_dict = peca_dict[0]
    
    return peca_dict



# print(query_get_peca('TS1-3-01'))
# print(query_get_ordem(504198))