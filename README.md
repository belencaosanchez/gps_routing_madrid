# GPS Routing System for Madrid

This project implements a GPS-style application that calculates optimal routes
in the street network of Madrid. The system allows users to compute different
types of routes between two addresses using graph algorithms and real geographic data.

The application was developed as an academic project for the course *Discrete Mathematics*
in the Bachelor in Mathematical Engineering and Artificial Intelligence.

---

## Project Description

The program allows the user to calculate optimal routes in the city of Madrid,
offering three different routing modes:

- Shortest route based on distance
- Fastest route based on travel time
- Fastest route considering expected traffic light delays

The system uses real street data from the Madrid City Council and OpenStreetMap,
and applies graph algorithms to compute optimal paths.

---

## Project Structure and Modules

The code is organized into multiple modules to improve clarity and maintainability:

### `gps.py`
Main application module.  
Handles user interaction, requests origin and destination addresses, and displays
navigation instructions and the selected route.

Includes functions for:
- Calculating edge weights based on distance
- Calculating travel time using maximum speed
- Estimating travel time including traffic light delays
- Finding the closest graph node to a geographic coordinate
- Generating navigation instructions
- Visualizing the selected route

---

### `callejero.py`
Auxiliary module responsible for loading and processing street data and the road network.

Main functionalities:
- Conversion of geographic coordinates from DMS format to decimal degrees
- Loading the Madrid street directory from a CSV file (`direcciones.csv`)
- Searching for specific addresses and retrieving their coordinates
- Downloading the Madrid road network from OpenStreetMap
- Processing the graph into a directed graph without loops
- Drawing the street graph using geographic coordinates

---

### `grafo_pesado.py`
Module containing implementations of graph algorithms used in the project.

Implemented algorithms:
- Dijkstra’s algorithm
- Minimum path calculation
- Prim’s algorithm
- Kruskal’s algorithm

These algorithms are used to compute optimal routes and analyze the graph structure.

---

## Data Structures Used

The project makes use of several data structures:

- **Pandas DataFrames**:  
  Used to load and process the Madrid street directory from a CSV file.

- **NetworkX Graphs**:  
  A directed graph is used to represent Madrid’s road network, where:
  - Nodes represent intersections or points on streets
  - Edges represent road segments with attributes such as length, street name, and maximum speed

- **Dictionaries and Lists**:  
  Used in the implementation of graph algorithms to store distances, parent nodes,
  routes, and navigation instructions.

---

## Route Calculation Process

1. The user enters origin and destination addresses in the format  
   `"Street type Street name, number"`.

2. The system searches the street directory and retrieves geographic coordinates
   for both addresses.

3. The closest nodes in the street graph are identified.

4. Dijkstra’s algorithm is applied using the selected cost function:
   - Distance-based
   - Time-based
   - Expected time including traffic lights

5. The optimal route is computed and returned as a sequence of nodes.

6. Navigation instructions are generated and displayed.

7. The route is visually highlighted on the map.

---

## Technologies and Libraries

- Python
- Pandas
- NetworkX
- OSMnx
- Matplotlib

---

## Academic Context

This project was developed as part of the *Discrete Mathematics* course  
at Universidad Pontificia Comillas (ICAI).

It demonstrates the application of graph theory algorithms to real-world
geospatial data and route optimization problems.

---

## References

- NetworkX Documentation  
- OSMnx: Python for Street Networks  
- OpenStreetMap  
- Matplotlib Documentation  
- Dijkstra, E. W. (1959). *A note on two problems in connexion with graphs*

