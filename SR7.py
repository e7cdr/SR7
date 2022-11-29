# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 10:50:04 2022

Legacy RA-RR

@author: E7C
"""

#Streamlit para webb local app
import streamlit as st
import pandas as pd
import numpy as np
import base64  # Standard Python Module
from io import StringIO, BytesIO  # Standard Python Module


def generate_excel_download_link(df3):
    # Credit Excel: https://discuss.streamlit.io/t/how-to-add-a-download-excel-csv-function-to-a-button/4474/5
    towrite = BytesIO()
    df3.to_excel(towrite, encoding="utf-8", index=False, header=True)  # write to BytesIO buffer
    towrite.seek(0)  # reset pointer
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="data_download.xlsx">Download Excel File</a>'
    return st.markdown(href, unsafe_allow_html=True)

#Libreria para interactuar con archivos office

"""
# SR7 - Combinador de archivos

Crea un archivo de excel haciendo matching entre dos tablas.

* Primero: Sube los archivos excel que contengan vaalores
           comunes por columnas
"""
RRR = st.file_uploader('Subir RRR', type=['xlsx', 'csv'])
if RRR:
    st.markdown('---')
    xlsxRRR = pd.read_excel(RRR, engine='openpyxl')
    xlsxRRR.rename(columns = {'Payment Gateway Authorisation':'Approval Code'}, inplace = True )
    df1 = xlsxRRR[["Approval Code","Order No.","Payee","Amount"]]
    st.dataframe(df1)
    
   
    
"""
* Segundo: Asegurate de que ambas tablas contengan al menos una 
           columna con el mismo nombre
"""

RADR = st.file_uploader('Subir RADR', type=['xlsx', 'csv'])
if RADR:
    st.markdown('---')
    xlsxRADR = pd.read_excel(RADR, engine='openpyxl')
    df2 = xlsxRADR[["Reference Number","Approval Code", "Amount (Applied)","Remarks"]]
    st.dataframe(df2)
    df2['Left'] = df2['Approval Code'].str[:6]  # LEFT() Equivalent

    #df2['Right'] = df2['Approval Code'].str[6:]  # RIGHT() Equivalent

#Para combinar dos archivos que tengan una columna de datos en comun. Inner = Interseccion

#Boton

boton1 = st.button("Combinar")
if boton1:
    df3 = df1.merge(df2, left_on='Approval Code', right_on='Approval Code', how='inner' )
    df3 = df3.drop_duplicates("Order No.") #Remover ordenes duplicadas
    amount = df3['Amount']*-1
    amountAppl = df3['Amount (Applied)']
    df3['Pending funds'] = amount - amountAppl
    df3['Type'] = np.where(df3['Pending funds'] == 0, 'Full refund', 'Partial refund')

# Part 2:

# Agregando columnas y formulas para el Pending funds y el Type

"""
# RESULTADO
"""
st.dataframe(df3)

#fondo de la pagina Downloads
st.subheader('Descargas:')
generate_excel_download_link(df3)


