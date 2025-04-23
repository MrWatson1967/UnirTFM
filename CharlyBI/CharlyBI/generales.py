
import pandas as pd
import numpy as np
import os 
import pyodbc

#Abre archivos en CSV y JSON
def CargarArchivo(url: str) -> pd.DataFrame: 
    # Obtener la extensión del archivo
    extension = os.path.splitext(url)

    #Carga el archivo
    if extension == '.json':
        df = pd.read_json(url, lines=True)
    elif extension == '.csv':
        df = pd.read_csv(url, sep="|")

    return df

#Borra del dataset filas sin datos
def EliminarFilasNulas(df_antes: pd.DataFrame) -> pd.DataFrame:

    # Calcular el 50% de las columnas
    threshold = df_antes.shape[1] * 0.5 

    # Eliminar filas con más del 50% de valores nulos
    df_nuevo = df_antes.dropna(thresh=threshold)

    return df_nuevo 

#Elimina columnas sin datos en todo el dataframe
def EliminarColumnasNulas(df_antes: pd.DataFrame) -> pd.DataFrame:
    # Calcular el 40% de las columnas nulas
    threshold = len(df_antes) * 0.60

    # Eliminar columnas con más del 40% de valores nulos
    df_nuevo = df_antes.dropna(axis=1, thresh=threshold)

    return df_nuevo 

#Graba un dataframe en archivo
def GrabarArchivo(url:str, tipo:str, df:pd.DataFrame):
    if tipo == 'CSV':
        # Guardar el DataFrame como un archivo CSV
        df.to_csv(url, sep=';', encoding='utf-8', index=False)
    else:
        # Guardar el DataFrame como un archivo JSON
        df.to_json(url, orient='records')

    return

#Elimina registros duplicados
def EliminarDuplicadosGlobales(df_antes: pd.DataFrame) -> pd.DataFrame:
 
    #Elimina duplicados basados en todas las columnas.
    df_nuevo = df_antes.drop_duplicates()    
 
    return df_nuevo 

#Elimina por llave duplicada
def EliminarDuplicadosClaves(df_antes: pd.DataFrame, llave:str) -> pd.DataFrame:

    #Elimina duplicados basado en la columnas clave.
    df_nuevo = df_antes.drop_duplicates(subset=[llave])

    return df_nuevo 

#Quita espacios en blanco por derecha, izquierda
def EliminarEspacios(df_antes: pd.DataFrame) -> pd.DataFrame:
    #Asigna nuevo dataset
    df_nuevo = df_antes 

    #Limpia espacios de variables tipo object
    df_nuevo[df_nuevo.select_dtypes(include=['object']).columns] = df_nuevo.select_dtypes(include=['object']).apply(lambda x: x.str.strip())

    #Limpia espacios de variables tipo string 
    df_nuevo[df_nuevo.select_dtypes(include=['string']).columns] = df_nuevo.select_dtypes(include=['string']).apply(lambda x: x.str.strip())

    return df_nuevo 

#Elimina valores nulos
def EliminarSiNulo(df_antes: pd.DataFrame, llave:str) -> pd.DataFrame:

    #Elimina filas con columnas clave en vacia
    df_nuevo = df_antes.dropna(subset=[llave])

    return df_nuevo 

#Transforma los NaN de columnas numericas en 0
def LimpiarDeNulos(df_antes: pd.DataFrame) -> pd.DataFrame:
    
    #Llenar los valores NaN en columnas numéricas con 0
    df_antes[df_antes.select_dtypes(include=[np.number]).columns] = df_antes.select_dtypes(include=[np.number]).fillna(0)

    #Llenar los valores NaN en columnas categóricas con 'NaN'
    df_antes[df_antes.select_dtypes(include=[object]).columns] = df_antes.select_dtypes(include=[object]).fillna('NaN')

    return df_antes

#Conectar a SQL Server
def conectar_sql_server():
    #Conecta a una base de datos SQL Server.
    
    try:
        conexion = pyodbc.connect(
            #"DRIVER={ODBC Driver 17 for SQL Server};"   # Driver
            "DRIVER={SQL Server};"                      # Driver
            "SERVER=.\\SQL002;"                         # Nombre del servidor
            "DATABASE=CharlyBi;"                        # Base de datos
            "UID=CharlyBI;"                             # Usuario
            "PWD=Inicio0000;"                           # Contraseña
            , autocommit=True
            ,timeout=30
        )
        return conexion
    except Exception as e:
        print(f"Error al conectar a SQL Server: {e}")
        return None

#Lee desde SQL Sever la vista seleccionada
def obtener_datos_vista(nombre_vista: str):
    #Obtiene datos desde una vista en SQL Server.
    
    try:
        conexion = conectar_sql_server()  # Conectar a SQL Server
        if not conexion:
            return []

        cursor = conexion.cursor()
        cursor.execute(f"SELECT Nombre FROM {nombre_vista}")  # Consultar la vista
        datos = [fila[0] for fila in cursor.fetchall()]  # Extraer los nombres
        cursor.close()
        conexion.close()

        return datos
    except Exception as e:
        print(f"Error al obtener datos de la vista {nombre_vista}: {e}")
        return []
    
#Lee desde SQL Server el Ranquin de Ventas
def obtener_ranking_ventas(eje_y: str, fecIni: str, fecfin: str, filtro: str, vrfiltro: str):

    try:
        conexion = conectar_sql_server()
        if not conexion:
            return []
    
        #Ejecuta procedimiento de calculo
        cursor = conexion.cursor()

        #Forzar los parametros a varchar para sql server
        eje_y = eje_y.strip()
        fecIni = fecIni.strip()
        fecfin = fecfin.strip()
        filtro = filtro.strip()
        vrfiltro = vrfiltro.strip()

        cursor.execute("{CALL prRanVen (?, ?, ?, ?, ?)}", (eje_y, fecIni, fecfin, filtro, vrfiltro)) #Ejecuta Procedimiento
        #cursor.execute("{CALL prRanVen (?, ?, ?, ?, ?)}", ("Puntos de Venta", "2022-01-01", "2022-12-31", "Todos", ""))       
        conexion.commit()
        cursor.close()
        
        #Extrae informacion
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM KPIranven")  
        datos = [{"Descripcion": fila[0], "Valor": fila[1]} for fila in cursor.fetchall()] 

        cursor.close()
        conexion.close()

        return datos
    except Exception as e:
        print(f"Error al obtener el ranking de ventas: {e}")
        return []

#Lee desde SQL Server el Ticket Promedio
def obtener_ticket_promedio(eje_y: str, fecIni: str, fecfin: str):

    try:
        conexion = conectar_sql_server()
        if not conexion:
            return []
    
        #Ejecuta procedimiento de calculo
        cursor = conexion.cursor()

        #Forzar los parametros a varchar para sql server
        eje_y = eje_y.strip()
        fecIni = fecIni.strip()
        fecfin = fecfin.strip()

        cursor.execute("{CALL prTicPro (?, ?, ? )}", (eje_y, fecIni, fecfin)) #Ejecuta Procedimiento
        conexion.commit()
        cursor.close()
        
        #Extrae informacion
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM KPIticpro")  
        datos = [{"Descripcion": fila[0], "TicketPromedio": fila[3]} for fila in cursor.fetchall()] 

        cursor.close()
        conexion.close()

        return datos
    except Exception as e:
        print(f"Error al obtener el ticket promedio: {e}")
        return []

#Lee desde SQL Server el Ticket Promedio
def obtener_upt(eje_y: str, fecIni: str, fecfin: str):

    try:
        conexion = conectar_sql_server()
        if not conexion:
            return []
    
        #Ejecuta procedimiento de calculo
        cursor = conexion.cursor()

        #Forzar los parametros a varchar para sql server
        eje_y = eje_y.strip()
        fecIni = fecIni.strip()
        fecfin = fecfin.strip()

        cursor.execute("{CALL prUpt (?, ?, ? )}", (eje_y, fecIni, fecfin)) #Ejecuta Procedimiento
        conexion.commit()
        cursor.close()
        
        #Extrae informacion
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM KPIupt")  
        datos = [{"Descripcion": fila[0], "UPT": fila[3]} for fila in cursor.fetchall()] 

        cursor.close()
        conexion.close()

        return datos
    except Exception as e:
        print(f"Error al obtener unidades por ticket: {e}")
        return []
