import csv

def addVertices(G: dict, vertices: list):
    
    for vertex in vertices:
        if vertex not in G:
            G[vertex] = []

def removeVertex(G, node):
    
    if node in G:
        del G[node]
    for n in G:
        for neighbor in G[n]:
            if neighbor[0] == node:
                G[n].remove(neighbor)

def addEdges(G: dict, edges: list):
    
    for edge in edges:
        G[edge[0]].append((edge[1], edge[2]))

def create_flight_network(filename: str, option: int):

    with open(filename, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)

    data = data[1:]
    data = [list(map(str, i)) for i in data]

    vertices = []
    edges = []

    # Option 1 represents the duration based graph
    if option == 1:
        G = {}
        for i in data:
            if i[0] not in vertices:
                vertices.append(i[0])
            if i[1] not in vertices:
                vertices.append(i[1])
        addVertices(G, vertices)

        for i in data:
            edges.append((i[0], i[1], int(i[2])))
        addEdges(G, edges)

    # Option 2 represents the distance based graph
    else:
        G = {}
        for i in data:
            if i[0] not in vertices:
                vertices.append(i[0])
            if i[1] not in vertices:
                vertices.append(i[1])
        addVertices(G, vertices)

        for i in data:
            edges.append((i[0], i[1], int(i[3])))
        addEdges(G, edges)

    return G

# Helper Function for getting neighbours of a node
def getOutgoingNeighbors(G, node):
        
    neighbors = []
    for edge in G[node]:
        neighbors.append(edge[0])

    return neighbors
    
def get_flight_connections(graph: dict, city: str, option: str) -> list:
    
    connections = []
    
    if city not in graph:
        return connections

    # Option 'i' represents incoming flights
    if option == 'i':
        for n in graph:
            if city in getOutgoingNeighbors(graph, n):
                connections.append(n)

    # Option 'o' represents outgoing flights            
    else:
        connections = getOutgoingNeighbors(graph, city)

    return connections     

def get_number_of_flight_connections(graph: dict, city: str, option: str) -> int:
    
    connections = get_flight_connections(graph, city, option)
    
    # Returns the Length of the list of connections
    return len(connections)

def get_flight_details(graph: dict, origin: str, destination: str) -> int:
    
    if origin not in graph:
        return None
    
    neighbours = []
    neighbours = getOutgoingNeighbors(graph, origin)
    
    if destination not in neighbours:
        return -1
    
    for edge in graph[origin]:
        if edge[0] == destination:
            return edge[1]

def add_flight(graph: dict, origin: str, destination: str, weight: int):
    
    if origin not in graph:
        return origin, "is not accessed by the Flight Network."
    
    if destination not in graph:
        return destination, "is not accessed by the Flight Network."

    neighbours = []
    neighbours = getOutgoingNeighbors(graph, origin)
    
    if destination not in neighbours:
        graph[origin].append((destination, weight))
    else:
        for edge in range(len(graph[origin])):
            if graph[origin][edge][0] == destination:
                graph[origin][edge] = (destination, weight)
                break

def add_airport(graph: dict, city: str, destination: str, weight: int):
    
    if city in graph:
        return 'This Airport already exists in the Flight Network.'
    
    edges = []
    vertex = []

    vertex.append(city)
    addVertices(graph, vertex)

    edges.append((city, destination, weight))
    addEdges(graph, edges)

def get_secondary_flights(graph: dict, city: str):
    
    if city not in graph:
        return None
    
    secondary_flights = []
    neighbours = []
    neighbours = getOutgoingNeighbors(graph, city)

    for neighbour in neighbours:
        for edge in graph[neighbour]:
            if edge[0] not in secondary_flights:
                secondary_flights.append(edge[0])
    
    return secondary_flights

def counting_common_airports(graph: dict, cityA: str, cityB: str) -> int:
        
    common_airports = 0
    neighboursA = []
    neighboursB = []
    neighboursA = getOutgoingNeighbors(graph, cityA)
    neighboursB = getOutgoingNeighbors(graph, cityB)

    for neighbourA in neighboursA:
        for neighbourB in neighboursB:
            if neighbourA == neighbourB:
                common_airports += 1
    
    return common_airports

def remove_flight(graph: dict, origin: str, destination: str):
        
    if origin not in graph:
        return origin, "is not accessed by the Flight Network."
        
    if destination not in graph:
        return destination, "is not accessed by the Flight Network."

    for edge in graph[origin]:
        if edge[0] == destination:
            graph[origin].remove(edge)

    for edge in graph[destination]:
        if edge[0] == origin:
            graph[destination].remove(edge)

def remove_airport(graph: dict, city: str):
    
    if city not in graph:
        return city, "is not accessed by the Flight Network."
    
    removeVertex(graph, city)

    return graph

def DFS_all_routes(graph: dict, origin: str, destination: str, route: list, all_routes: list):

    route.append(origin)
 
    if origin == destination:
        all_routes.append(route.copy())
    else:
        for neighbor in getOutgoingNeighbors(graph, origin):
            if neighbor not in route:
                all_routes = DFS_all_routes(graph, neighbor, destination, route, all_routes)
    
    route.pop()
    
    # route = [(origin, [origin])]

    # while route:
    #     (vertex, path) = route.pop()
    #     for neighbor in getOutgoingNeighbors(graph, vertex):
    #         if neighbor == destination:
    #             all_routes.append(path + [neighbor])
    #         elif neighbor not in path:
    #             route.append((neighbor, path + [neighbor]))

    return all_routes

def find_all_routes(graph: dict, origin: str, destination: str):
    
    all_routes = []
    route = []

    if origin not in graph:
        return None
    
    if destination not in graph: 
        return None
    
    if destination == origin:
        return all_routes
        
    all_routes = DFS_all_routes(graph, origin, destination, route, all_routes)
    return all_routes

def DFS_layovers(graph: dict, origin: str, destination: str, route: list, layovers_lst: list):
    
    route.append(origin)

    if origin == destination:
        layovers_lst.append(len(route) - 2)
    else:
        for neighbor in getOutgoingNeighbors(graph, origin):
            if neighbor not in route:
                layovers_lst = DFS_layovers(graph, neighbor, destination, route, layovers_lst)
    route.pop()

    return layovers_lst

def find_number_of_layovers(graph: dict, origin: str, destination: str):
    
    layovers_lst = []
    route = []

    if origin not in graph:
        return None
    
    if destination not in graph: 
        return None
    
    if destination == origin:
        return layovers_lst
    
    layovers_lst = DFS_layovers(graph, origin, destination, route, layovers_lst)
    
    # Applying Selection Sort (.sort() was not working for some reason)
    for i in range(len(layovers_lst)):
        min = i
        for j in range(i+1, len(layovers_lst)):
            if layovers_lst[j] < layovers_lst[min]:
                min = j
        layovers_lst[i], layovers_lst[min] = layovers_lst[min], layovers_lst[i]
    
    return layovers_lst

def main():

    option = 2
    filename = 'flight_network.csv'
    G = create_flight_network(filename, option)
    # print(G)

    # print(get_secondary_flights(G, "Dubai"))

    # print(get_flight_details(G, "Dubai", 'Karachi'))

    # print()
    # print()

    # add_airport(G, "Karachi", "Dubai", 130)
    # print(G)

    # city = 'Caracas'
    # option = 'i'
    # print(get_flight_connections(G, city, option))

    # origin = 'Dubai'
    # destination = 'Seattle'
    # print(get_flight_details(G, origin, destination))

    # print(get_secondary_flights(G, "Dubai"))

    # remove_flight(G, "Dubai", "Seattle")

    # print(find_all_routes(G, "Dubai", "Seattle"))
    # should output the following:
    # [['Dubai', 'Seattle', 'Dubai'], ['Dubai', 'Seattle', 'Boston', 'Dubai'], ['Dubai', 'Boston', 'Seattle', 'Dubai'], ['Dubai', 'Boston', 'Dubai'], ['Dubai', 'Seattle', 'Boston', 'Seattle', 'Dubai'], ['Dubai', 'Boston', 'Seattle', 'Boston', 'Dubai'], ['Dubai', 'Boston', 'Seattle', 'Dubai'], ['Dubai', 'Seattle', 'Boston', 'Seattle', 'Boston', 'Dubai'], ['Dubai', 'Boston', 'Seattle', 'Boston', 'Seattle', 'Dubai'], ['Dubai', 'Boston', 'Seattle', 'Boston', 'Dubai'], ['Dubai', 'Boston', 'Seattle', 'Boston', 'Seattle', 'Boston', 'Dubai']]

    # print(find_number_of_layovers(G, "Dubai", "Seattle"))

    # print(G)

if __name__ == '__main__':
    main()