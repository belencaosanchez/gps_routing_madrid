"""
callejero.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Grupo: GPxxx
Integrantes:
    - XX
    - XX

Descripción:
Librería con herramientas y clases auxiliares necesarias para la representación de un callejero en un grafo.

Complétese esta descripción según las funcionalidades agregadas por el grupo.
"""

import osmnx as ox
import networkx as nx
import pandas as pd
import os.path
import matplotlib.pyplot as plt

from typing import Tuple

STREET_FILE_NAME="direcciones.csv"

PLACE_NAME = "Madrid, Spain"
MAP_FILE_NAME="madrid.graphml"

MAX_SPEEDS={'living_street': '20',
 'residential': '30',
 'primary_link': '40',
 'unclassified': '40',
 'secondary_link': '40',
 'trunk_link': '40',
 'secondary': '50',
 'tertiary': '50',
 'primary': '50',
 'trunk': '50',
 'tertiary_link':'50',
 'busway': '50',
 'motorway_link': '70',
 'motorway': '100'}


class ServiceNotAvailableError(Exception):
    "Excepción que indica que la navegación no está disponible en este momento"
    pass


class AdressNotFoundError(Exception):
    "Excepción que indica que una dirección buscada no existe en la base de datos"
    pass


############## Parte 2 ##############


# Función para convertir DMS a decimal
def dms_to_decimal(dms_str: str) -> float:
    """
    Convierte una coordenada DMS a grados decimales.
    """
    try:
        parts = dms_str.replace('°', ' ').replace("'", ' ').replace('"', ' ').split()
        degrees, minutes, seconds, direction = float(parts[0]), float(parts[1]), float(parts[2]), parts[3]
        decimal = degrees + minutes / 60 + seconds / 3600
        return -decimal if direction in ['S', 'W'] else decimal
    except Exception as e:
        raise ValueError(f"Error al convertir DMS a decimal: {e}")


def carga_callejero() -> pd.DataFrame:
    """ 
    Función que carga el callejero de Madrid, lo procesa y devuelve
    un DataFrame con los datos procesados.
    """
    STREET_FILE_NAME = "direcciones.csv"

    if not os.path.exists(STREET_FILE_NAME):
        raise FileNotFoundError(f"El archivo {STREET_FILE_NAME} no existe.")

    # Mostrar los nombres de las columnas disponibles para depuración
    try:
        df_raw = pd.read_csv(STREET_FILE_NAME, sep=";", encoding="latin1")
        print("Columnas encontradas en el archivo:", df_raw.columns)
    except Exception as e:
        raise ValueError(f"Error al leer el archivo completo: {e}")

    # Columnas que queremos mantener (ajústalas según los nombres reales del CSV)
    columns_to_keep = ["VIA_CLASE", "VIA_PAR", "VIA_NOMBRE", "NUMERO", "LATITUD", "LONGITUD"]

    # Leer solo las columnas requeridas
    try:
        df = pd.read_csv(STREET_FILE_NAME, sep=";", encoding="latin1", usecols=columns_to_keep)
    except Exception as e:
        raise ValueError(f"Error al leer las columnas específicas: {e}")

    # Renombrar columnas
    df.rename(columns={
        "VIA_CLASE": "clase_via",
        "VIA_PAR": "particula_via",
        "VIA_NOMBRE": "nombre_via",
        "NUMERO": "numero",
        "LATITUD": "latitud",
        "LONGITUD": "longitud"
    }, inplace=True)

    # Convertir LATITUD y LONGITUD de DMS a decimales
    try:
        df["latitud"] = df["latitud"].apply(dms_to_decimal)
        df["longitud"] = df["longitud"].apply(dms_to_decimal)
    except Exception as e:
        raise ValueError(f"Error al convertir coordenadas: {e}")

    return df




def busca_direccion(direccion:str, callejero:pd.DataFrame) -> Tuple[float,float]:
    """ Función que busca una dirección, dada en el formato
        calle, numero
    en el DataFrame callejero de Madrid y devuelve el par (latitud, longitud) en grados de la
    hubicación geográfica de dicha dirección
    
    Args:
        direccion (str): Nombre completo de la calle con número, en formato "Calle, num"
        callejero (DataFrame): DataFrame con la información de las calles
    Returns:
        Tuple[float,float]: Par de float (latitud,longitud) de la dirección buscada, expresados en grados
    Raises:
        AdressNotFoundError: Si la dirección no existe en la base de datos
    Example:
        busca_direccion("Calle de Alberto Aguilera, 23", data)=(40.42998055555555,3.7112583333333333)
        busca_direccion("Calle de Alberto Aguilera, 25", data)=(40.43013055555555,3.7126916666666667)
    """

    class AdressNotFoundError(Exception):
        pass


    try:
        # Validar formato de la dirección
        if ", " not in direccion:
            raise ValueError("Formato de dirección inválido. Use 'Calle, número'.")
 
        # Separar la dirección en clase de vía, nombre y número
        via, numero = direccion.split(", ")
        numero = int(numero)  # Convertir el número a entero
        via_split = via.split(" ", 1)
        clase = via_split[0].strip()
        nombre = via_split[-1].strip()
 
        # Combinar particula_via y nombre_via en el DataFrame para búsqueda
        if "particula_via" in callejero.columns and "nombre_via" in callejero.columns:
            callejero["nombre_completo"] = (
                callejero["particula_via"].fillna("") + " " + callejero["nombre_via"]
            ).str.strip()
        else:
            raise KeyError("El DataFrame no contiene las columnas necesarias para formar el nombre completo.")
 
        # Filtrar el DataFrame por clase de vía, nombre y número
        match = callejero[
            (callejero["clase_via"].str.contains(clase, case=False, na=False)) &
            (callejero["nombre_completo"].str.contains(nombre, case=False, na=False)) &
            (callejero["numero"] == numero)
        ]
 
        # Comprobar si hay coincidencias
        if match.empty:
            raise AdressNotFoundError(f"No se encontró la dirección: {direccion}")
 
        # Retornar las coordenadas de la primera coincidencia
        return match.iloc[0]["latitud"], match.iloc[0]["longitud"]
 
    except ValueError as ve:
        raise AdressNotFoundError(f"Formato inválido para la dirección '{direccion}'. {ve}")
    except KeyError as ke:
        raise AdressNotFoundError(f"Error en las columnas del DataFrame: {ke}")
    except Exception as e:
        raise AdressNotFoundError(f"Error inesperado al buscar la dirección: {e}")




############## Parte 4 ##############


def carga_grafo() -> nx.MultiDiGraph:
    """
    Descarga o carga el grafo de Madrid desde OpenStreetMap.
    
    Returns:
        nx.MultiDiGraph: Grafo descargado o cargado.
    Raises:
        ServiceNotAvailableError: Si no es posible descargar el grafo.
    """
    try:
        if os.path.exists(MAP_FILE_NAME):
            return ox.load_graphml(MAP_FILE_NAME)
        else:
            grafo = ox.graph_from_place(PLACE_NAME, network_type="drive")
            ox.save_graphml(grafo, MAP_FILE_NAME)
            return grafo
    except Exception as e:
        raise ServiceNotAvailableError(f"No fue posible recuperar el grafo: {e}")
 
 
def procesa_grafo(multidigrafo: nx.MultiDiGraph) -> nx.DiGraph:
    """
    Convierte un MultiDiGraph en un DiGraph dirigido sin bucles.
 
    Args:
        multidigrafo (nx.MultiDiGraph): Multidigrafo de calles.
    Returns:
        nx.DiGraph: Grafo dirigido sin bucles.
    """
    # Crear un nuevo DiGraph desde el MultiDiGraph
    digraph = nx.DiGraph()
 
    # Copiar nodos con sus atributos
    digraph.add_nodes_from(multidigrafo.nodes(data=True))
 
    # Copiar aristas eliminando duplicados y bucles
    for u, v, data in multidigrafo.edges(data=True):
        if u != v:  # Eliminar bucles
            if not digraph.has_edge(u, v):
                digraph.add_edge(u, v, **data)
 
    return digraph
 
 
def dibuja_grafo(grafo: nx.DiGraph):
    """
    Dibuja el grafo en base a sus coordenadas geográficas.
    
    Args:
        grafo (nx.DiGraph): Grafo a dibujar.
    """
    import matplotlib.pyplot as plt
 
 
def dibuja_grafo(grafo: nx.DiGraph):
    """
    Dibuja el grafo en base a sus coordenadas geográficas utilizando draw_networkx_edges y draw_networkx_nodes.
 
    Args:
        grafo (nx.DiGraph): Grafo a dibujar.
    """
    # Obtener las posiciones geográficas de los nodos
    pos = {node: (data["x"], data["y"]) for node, data in grafo.nodes(data=True)}
 
    # Crear figura
    plt.figure(figsize=(12, 12))
 
    # Dibujar aristas
    nx.draw_networkx_edges(
        grafo,
        pos,
        edge_color="gray",
        alpha=0.2,
        width=0.5
    )
 
    # Dibujar nodos
    nx.draw_networkx_nodes(
        grafo,
        pos,
        node_size=5,
        node_color="blue",
        alpha=0.2
    )
 
    # Configurar gráfico
    plt.title("Grafo de calles de Madrid")  # Título
    plt.axis("off")  # Ocultar ejes
    plt.show()
