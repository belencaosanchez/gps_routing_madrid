# GPS Routing System for Madrid

Este proyecto implementa un programa GPS que permite calcular rutas óptimas en el
callejero de Madrid. El sistema ofrece al usuario distintas opciones de ruta entre
dos direcciones, utilizando algoritmos de grafos y datos geográficos reales.

El proyecto fue desarrollado como trabajo académico para la asignatura
**Matemática Discreta** del Grado en Ingeniería Matemática e Inteligencia Artificial.

---

## Descripción del Proyecto

El programa permite calcular rutas óptimas en la ciudad de Madrid, ofreciendo
tres tipos distintos de rutas en función de las preferencias del usuario:

- Ruta más corta en términos de distancia  
- Ruta más rápida en términos de tiempo  
- Ruta más rápida considerando el tiempo esperado debido a semáforos  

El sistema utiliza datos reales del callejero de Madrid obtenidos del Ayuntamiento
de Madrid y de OpenStreetMap, aplicando algoritmos de grafos para el cálculo de
caminos mínimos.

---

## Organización del Código y Módulos

El código se ha dividido en distintos módulos con el objetivo de mejorar la
claridad, la organización y el mantenimiento del programa.

### `gps.py`
Módulo principal del programa.  
Se encarga de la interacción con el usuario, solicitando las direcciones de origen
y destino, mostrando las instrucciones de navegación y representando la ruta
calculada.

Incluye funciones para:
- Calcular el peso de las aristas en función de la distancia
- Calcular el peso en función del tiempo de recorrido
- Calcular el tiempo esperado teniendo en cuenta semáforos
- Encontrar el nodo del grafo más cercano a unas coordenadas
- Generar instrucciones detalladas de navegación
- Visualizar la ruta sobre el grafo

---

### `callejero.py`
Módulo auxiliar encargado de la carga y procesamiento del callejero de Madrid,
así como de la construcción y tratamiento del grafo de la red vial.

Principales funcionalidades:
- Conversión de coordenadas geográficas del formato DMS a grados decimales
- Carga del callejero desde el archivo `direcciones.csv`
- Búsqueda de direcciones y obtención de sus coordenadas
- Descarga del grafo de Madrid desde OpenStreetMap
- Procesamiento del grafo para convertirlo en un grafo dirigido sin bucles
- Representación gráfica del grafo utilizando coordenadas geográficas

---

### `grafo_pesado.py`
Módulo que contiene las implementaciones de los algoritmos de grafos necesarios
para el cálculo de rutas óptimas.

Algoritmos implementados:
- Algoritmo de Dijkstra
- Cálculo del camino mínimo
- Algoritmo de Prim
- Algoritmo de Kruskal

Estos algoritmos se utilizan para calcular los caminos óptimos y analizar la
estructura del grafo.

---

## Estructuras de Datos Utilizadas

El programa utiliza diversas estructuras de datos para el manejo de la información:

- **DataFrames de Pandas**:  
  Utilizados para cargar y procesar el callejero de Madrid desde el archivo
  `direcciones.csv`.

- **Grafos de NetworkX**:  
  Se utiliza un grafo dirigido para representar la red vial de Madrid, donde:
  - Los nodos representan intersecciones o puntos de las vías
  - Las aristas representan tramos de carretera con atributos como longitud,
    nombre de la calle o velocidad máxima

- **Diccionarios y Listas**:  
  Utilizados en los algoritmos de grafos para almacenar distancias, nodos padre,
  rutas calculadas e instrucciones de navegación.

---

## Proceso de Cálculo de la Ruta Óptima

1. El usuario introduce las direcciones de origen y destino en el formato  
   `"Tipo de vía Nombre de la vía, número"`.

2. El sistema busca dichas direcciones en el callejero y obtiene sus coordenadas
   geográficas (latitud y longitud).

3. Se identifican los nodos del grafo más cercanos a las coordenadas obtenidas.

4. Se aplica el algoritmo de Dijkstra utilizando la función de coste seleccionada:
   - Distancia
   - Tiempo
   - Tiempo esperado considerando semáforos

5. Se calcula la ruta óptima entre el origen y el destino.

6. Se generan las instrucciones de navegación correspondientes.

7. La ruta se representa gráficamente sobre el grafo.

---

## Tecnologías y Librerías

- Python
- Pandas
- NetworkX
- OSMnx
- Matplotlib

Las dependencias del proyecto se encuentran especificadas en el archivo
`requirements.txt`.

---

## Contexto Académico

Este proyecto ha sido desarrollado como parte de la asignatura **Matemática
Discreta** en la Universidad Pontificia Comillas (ICAI).

El trabajo demuestra la aplicación de algoritmos de teoría de grafos a datos
geoespaciales reales para la resolución de problemas de optimización de rutas.

---

## Referencias

- Documentación de NetworkX  
- OSMnx: Python for Street Networks  
- OpenStreetMap  
- Documentación de Matplotlib  
- Dijkstra, E. W. (1959). *A note on two problems in connexion with graphs*
