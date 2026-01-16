"""
gps.py
 
Aplicación GPS que permite calcular rutas en el callejero de Madrid.

Grupo GP08A - Carolina Garicano Vidal ¬ María Belén Cao Sánchez
"""

 
import networkx as nx
import matplotlib.pyplot as plt
from callejero import (
    carga_callejero,
    carga_grafo,
    procesa_grafo,
    busca_direccion,
    MAX_SPEEDS
)
from grafo_pesado import camino_minimo
 
 
def calcula_peso_longitud(G: nx.Graph, u, v) -> float:
    """Calcula el peso de una arista basado en su longitud."""
    return G[u][v].get("length", 0)
 
 
def calcula_peso_tiempo(G: nx.Graph, u, v) -> float:
    """Calcula el peso de una arista basado en el tiempo estimado de viaje."""
    longitud = G[u][v].get("length", 0)
    velocidad_maxima = G[u][v].get("maxspeed", MAX_SPEEDS.get(G[u][v].get("highway", ""), 50))
    return longitud / (velocidad_maxima / 3.6)  # Convertir km/h a m/s
 
 
def calcula_peso_tiempo_esperado(G: nx.Graph, u, v) -> float:
    """Calcula el peso de una arista considerando tiempos de semáforo."""
    tiempo_base = calcula_peso_tiempo(G, u, v)
    prob_parada = 0.8
    tiempo_semáforo = 30  # en segundos
    return tiempo_base + prob_parada * tiempo_semáforo
 
 
def encuentra_nodo_mas_cercano(G: nx.Graph, lat: float, lon: float) -> object:
    """Encuentra el nodo más cercano a unas coordenadas."""
    menor_distancia = float("inf")
    nodo_cercano = None
 
    for nodo, data in G.nodes(data=True):
        distancia = ((data["y"] - lat) ** 2 + (data["x"] - lon) ** 2) ** 0.5
        if distancia < menor_distancia:
            menor_distancia = distancia
            nodo_cercano = nodo
 
    return nodo_cercano
 
 
def genera_instrucciones(G: nx.Graph, ruta: list) -> list:
    """Genera instrucciones detalladas para navegar por una ruta."""
    instrucciones = []
    distancia_actual = 0
    calle_actual = None
 
    for i in range(len(ruta) - 1):
        u, v = ruta[i], ruta[i + 1]
        calle = G[u][v].get("name", "vía desconocida")
        distancia = G[u][v].get("length", 0)
 
        if calle_actual is None:
            calle_actual = calle
            distancia_actual = distancia
        elif calle != calle_actual:
            instrucciones.append(f"Continúe por {calle_actual} durante {int(distancia_actual)} metros.")
            giro = "gire a la izquierda" if i % 2 == 0 else "gire a la derecha"  # Simulación de giros
            instrucciones.append(f"{giro} hacia {calle}.")
            calle_actual = calle
            distancia_actual = distancia
        else:
            distancia_actual += distancia
 
    if calle_actual:
        instrucciones.append(f"Continúe por {calle_actual} durante {int(distancia_actual)} metros hasta su destino.")
    return instrucciones
 
 
def resalta_ruta(G: nx.Graph, ruta: list):
    """Dibuja el grafo y resalta la ruta elegida."""
    pos = {nodo: (data["x"], data["y"]) for nodo, data in G.nodes(data=True)}
 
    plt.figure(figsize=(12, 12))
    nx.draw(G, pos, node_size=10, edge_color="gray", width=0.5, alpha=0.7, with_labels=False)
    ruta_edges = [(ruta[i], ruta[i + 1]) for i in range(len(ruta) - 1)]
    nx.draw_networkx_edges(G, pos, edgelist=ruta_edges, edge_color="red", width=2)
    plt.title("Ruta resaltada")
    plt.show()
 
 
def main():
    # Cargar el callejero y el grafo
    print("Cargando datos...")
    callejero = carga_callejero()
    grafo = procesa_grafo(carga_grafo())
 
    continuar = True
    while continuar:
        # Seleccionar origen
        origen_input = input("Ingrese la dirección de origen (o presione Enter para salir): ")
        if not origen_input:
            continuar = False
            continue
 
        try:
            lat_origen, lon_origen = busca_direccion(origen_input, callejero)
        except Exception as e:
            print(f"Error al buscar la dirección de origen: {e}")
            continuar = True
            continue
 
        # Seleccionar destino
        destino_input = input("Ingrese la dirección de destino (o presione Enter para salir): ")
        if not destino_input:
            continuar = False
            continue
 
        try:
            lat_destino, lon_destino = busca_direccion(destino_input, callejero)
        except Exception as e:
            print(f"Error al buscar la dirección de destino: {e}")
            continuar = True
            continue
 
        # Encontrar nodos más cercanos
        origen = encuentra_nodo_mas_cercano(grafo, lat_origen, lon_origen)
        destino = encuentra_nodo_mas_cercano(grafo, lat_destino, lon_origen)
 
        # Seleccionar modo de cálculo
        print("Seleccione el modo de cálculo:")
        print("1. Ruta más corta (distancia)")
        print("2. Ruta más rápida (tiempo)")
        print("3. Ruta más rápida con semáforos (tiempo esperado)")
        modo = input("Ingrese una opción (1/2/3): ")
 
        peso = None
        if modo == "1":
            peso = calcula_peso_longitud
        elif modo == "2":
            peso = calcula_peso_tiempo
        elif modo == "3":
            peso = calcula_peso_tiempo_esperado
        else:
            print("Opción no válida. Intente nuevamente.")
            continuar = True
            continue
 
        # Calcular ruta

        try:
            ruta = camino_minimo(grafo, origen, destino, peso)
            print("Ruta calculada exitosamente.")
        except Exception as e:
            print(f"Error al calcular la ruta: {e}")
            continuar = True
            continue
 
        # Generar y mostrar instrucciones
        instrucciones = genera_instrucciones(grafo, ruta)
        print("\nInstrucciones para la ruta:")
        for instruccion in instrucciones:
            print("-", instruccion)
 
        # Resaltar ruta en el grafo
        resalta_ruta(grafo, ruta)
 
    print("Gracias por usar el GPS. ¡Hasta luego!")
 
 
main()

