"""
grafo_pesado.py

Implementación de algoritmos de grafos:
1. Dijkstra
2. Camino mínimo
3. Prim
4. Kruskal

Grupo GP08A - Carolina Garicano Vidal ¬ María Belén Cao Sánchez
"""

import networkx as nx
from typing import Callable, Dict, List, Tuple


def dijkstra(G: nx.Graph, origen: object, peso: Callable[[nx.Graph, object, object], float]) -> Dict[object, object]:
    """
    Calcula el árbol de caminos mínimos usando el algoritmo de Dijkstra.

    Args:
        G (nx.Graph): Grafo no dirigido o dirigido.
        origen (object): Nodo inicial.
        peso (Callable): Función que calcula el peso de una arista.

    Returns:
        Dict[object, object]: Diccionario que indica el padre de cada nodo en el árbol de caminos mínimos.
    """
    distancia = {}
    padre = {}
    visitados = set()

    # Inicializar distancias y padres
    for nodo in G.nodes():
        distancia[nodo] = float('inf')
        padre[nodo] = None
    distancia[origen] = 0

    while len(visitados) < len(G.nodes()):
        # Seleccionar el nodo no visitado con menor distancia
        nodo_actual = None
        menor_distancia = float('inf')

        for nodo in G.nodes():
            if nodo not in visitados and distancia[nodo] < menor_distancia:
                menor_distancia = distancia[nodo]
                nodo_actual = nodo

        # Condición para terminar si no hay más nodos alcanzables
        if nodo_actual is None:
            visitados.update(G.nodes())  # Marcar todos los nodos como visitados para salir del bucle
            continue

        visitados.add(nodo_actual)

        # Actualizar distancias de los vecinos
        for vecino in G.neighbors(nodo_actual):
            if vecino not in visitados:
                peso_arista = peso(G, nodo_actual, vecino)
                if distancia[nodo_actual] + peso_arista < distancia[vecino]:
                    distancia[vecino] = distancia[nodo_actual] + peso_arista
                    padre[vecino] = nodo_actual

    return padre


def camino_minimo(G: nx.Graph, origen: object, destino: object, peso: Callable[[nx.Graph, object, object], float]) -> List[object]:
    """
    Calcula el camino mínimo entre dos nodos usando Dijkstra.

    Args:
        G (nx.Graph): Grafo no dirigido o dirigido.
        origen (object): Nodo de inicio.
        destino (object): Nodo de destino.
        peso (Callable): Función que calcula el peso de una arista.

    Returns:
        List[object]: Lista de nodos que representan el camino mínimo.
    """
    padre = dijkstra(G, origen, peso)
    camino = []
    actual = destino

    while actual is not None:
        camino.append(actual)
        actual = padre[actual]

    camino.reverse()

    if len(camino) == 0 or camino[0] != origen:
        raise ValueError(f"No hay camino entre {origen} y {destino}.")

    return camino


def prim(G: nx.Graph, peso: Callable[[nx.Graph, object, object], float]) -> Dict[object, object]:
    """
    Calcula el árbol abarcador mínimo usando el algoritmo de Prim.

    Args:
        G (nx.Graph): Grafo no dirigido.
        peso (Callable): Función que calcula el peso de una arista.

    Returns:
        Dict[object, object]: Diccionario que indica el padre de cada nodo en el árbol.
    """
    nodos = list(G.nodes())
    if not nodos:
        return {}

    origen = nodos[0]
    padre = {}
    distancia = {}
    visitados = set()

    # Inicializar distancias y padres
    for nodo in G.nodes():
        distancia[nodo] = float('inf')
        padre[nodo] = None
    distancia[origen] = 0

    while len(visitados) < len(G.nodes()):
        nodo_actual = None
        menor_distancia = float('inf')

        for nodo in G.nodes():
            if nodo not in visitados and distancia[nodo] < menor_distancia:
                menor_distancia = distancia[nodo]
                nodo_actual = nodo

        # Condición para terminar si no hay más nodos alcanzables
        if nodo_actual is None:
            visitados.update(G.nodes())  # Marcar todos los nodos como visitados para salir del bucle
            continue

        visitados.add(nodo_actual)

        for vecino in G.neighbors(nodo_actual):
            if vecino not in visitados:
                peso_arista = peso(G, nodo_actual, vecino)
                if peso_arista < distancia[vecino]:
                    distancia[vecino] = peso_arista
                    padre[vecino] = nodo_actual

    return padre


def kruskal(G: nx.Graph, peso: Callable[[nx.Graph, object, object], float]) -> List[Tuple[object, object]]:
    """
    Calcula el árbol abarcador mínimo usando el algoritmo de Kruskal.

    Args:
        G (nx.Graph): Grafo no dirigido.
        peso (Callable): Función que calcula el peso de una arista.

    Returns:
        List[Tuple[object, object]]: Lista de aristas del árbol abarcador mínimo.
    """
    aristas = []
    padre = {}
    rango = {}

    # Inicializar conjuntos disjuntos
    for nodo in G.nodes():
        padre[nodo] = nodo
        rango[nodo] = 0

    def find(nodo):
        if padre[nodo] != nodo:
            padre[nodo] = find(padre[nodo])
        return padre[nodo]

    def union(nodo1, nodo2):
        raiz1 = find(nodo1)
        raiz2 = find(nodo2)

        if raiz1 != raiz2:
            if rango[raiz1] > rango[raiz2]:
                padre[raiz2] = raiz1
            elif rango[raiz1] < rango[raiz2]:
                padre[raiz1] = raiz2
            else:
                padre[raiz2] = raiz1
                rango[raiz1] += 1

    for u, v, data in sorted(G.edges(data=True), key=lambda e: peso(G, e[0], e[1])):
        if find(u) != find(v):
            union(u, v)
            aristas.append((u, v))

    return aristas


