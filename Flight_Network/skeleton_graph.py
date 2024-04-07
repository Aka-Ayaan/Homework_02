import csv

def addVertices(G: dict, vertices: list):  # Helper Function for adding Vertices
    
    for vertex in vertices:
        if vertex not in G:
            G[vertex] = []

def removeVertex(G, node):   # Helper Function for removing Vertices
    
    if node in G:
        del G[node]
    for n in G:
        for neighbor in G[n]:
            if neighbor[0] == node:
                G[n].remove(neighbor)

def addEdges(G: dict, edges: list):   # Helper Function for adding Edges
    
    for edge in edges:
        G[edge[0]].append((edge[1], edge[2]))

def create_flight_network(filename: str, option: int):

    # Reading the CSV file
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)

    # Removing the Header
    data = data[1:]
    data = [list(map(str, i)) for i in data]

    vertices = []   # List of nodes
    edges = []   # List of edges

    # Option 1 (duration based graph)
    if option == 1:
        G = {}

        # Adding Vertices
        for i in data:
            if i[0] not in vertices:
                vertices.append(i[0])
            if i[1] not in vertices:
                vertices.append(i[1])
        addVertices(G, vertices)

        # Adding Edges
        for i in data:
            edges.append((i[0], i[1], int(i[2])))
        addEdges(G, edges)

    # Option 2 (distance based graph)
    else:
        G = {}

        # Adding Vertices
        for i in data:
            if i[0] not in vertices:
                vertices.append(i[0])
            if i[1] not in vertices:
                vertices.append(i[1])
        addVertices(G, vertices)

        # Adding Edges
        for i in data:
            edges.append((i[0], i[1], int(i[3])))
        addEdges(G, edges)

    return G

def getOutgoingNeighbors(G, node):   # Helper Function for getting neighbours of a node
        
    neighbors = []
    for edge in G[node]:
        neighbors.append(edge[0])

    return neighbors
    
def get_flight_connections(graph: dict, city: str, option: str) -> list:
    
    connections = []
    
    # Checking if the city is in the graph
    if city not in graph:
        return connections

    # Option 'i' (incoming)
    if option == 'i':
        for n in graph:
            if city in getOutgoingNeighbors(graph, n):
                connections.append(n)

    # Option 'o' (outgoing)            
    else:
        connections = getOutgoingNeighbors(graph, city)

    return connections     

def get_number_of_flight_connections(graph: dict, city: str, option: str) -> int:
    
    connections = get_flight_connections(graph, city, option)
    
    # Returns the Length of the list of connections
    return len(connections)

def get_flight_details(graph: dict, origin: str, destination: str) -> int:
    
    # Checking if the origin is in the graph
    if origin not in graph:
        return None
    
    neighbours = []
    neighbours = getOutgoingNeighbors(graph, origin)
    
    # Checking if the destination is in the neighbours of the origin
    if destination not in neighbours:
        return -1
    
    # Returning the weight of the edge between the origin and the destination
    for edge in graph[origin]:
        if edge[0] == destination:
            return edge[1]

def add_flight(graph: dict, origin: str, destination: str, weight: int):
    
    # Checking if the origin is in the graph
    if origin not in graph:
        return origin, "is not accessed by the Flight Network."
    
    # Checking if the destination is in the graph
    if destination not in graph:
        return destination, "is not accessed by the Flight Network."

    neighbours = []
    neighbours = getOutgoingNeighbors(graph, origin)
    
    # Adding the flight between the origin and the destination
    if destination not in neighbours:
        graph[origin].append((destination, weight))
    
    # Updating the weight if the flight already exists
    else:
        for edge in range(len(graph[origin])):
            if graph[origin][edge][0] == destination:
                graph[origin][edge] = (destination, weight)
                break

def add_airport(graph: dict, city: str, destination: str, weight: int):
    
    # Checking if the city already exists in the graph
    if city in graph:
        return 'This Airport already exists in the Flight Network.'
    
    edges = []
    vertex = []

    # Adding the city to the graph
    vertex.append(city)
    addVertices(graph, vertex)

    # Adding the flight between the new city and the destination
    edges.append((city, destination, weight))
    addEdges(graph, edges)

def get_secondary_flights(graph: dict, city: str):
    
    # Checking if the city is in the graph
    if city not in graph:
        return None
    
    secondary_flights = []
    neighbours = []
    neighbours = getOutgoingNeighbors(graph, city)

    # Getting the neighbours of the neighbours of the city
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

    # Counting the common airports between the neighbours of cityA and cityB by comparison
    for neighbourA in neighboursA:
        for neighbourB in neighboursB:
            if neighbourA == neighbourB:
                common_airports += 1
    
    return common_airports

def remove_flight(graph: dict, origin: str, destination: str):
        
    # Checking if the origin is in the graph    
    if origin not in graph:
        return origin, "is not accessed by the Flight Network."

    # Checking if the destination is in the graph    
    if destination not in graph:
        return destination, "is not accessed by the Flight Network."

    # Removing the flight between the origin and the destination
    for edge in graph[origin]:
        if edge[0] == destination:
            graph[origin].remove(edge)

    # Removing the flight between the destination and the origin
    for edge in graph[destination]:
        if edge[0] == origin:
            graph[destination].remove(edge)

def remove_airport(graph: dict, city: str):
    
    # Checking if the city is in the graph
    if city not in graph:
        return city, "is not accessed by the Flight Network."
    
    # Removing the city from the graph
    removeVertex(graph, city)

    return graph

def DFS_all_routes(graph: dict, origin: str, destination: str, route: list, all_routes: list):

    # starting from the origin
    route.append(origin)
 
    # Base Case - adds the route to the list if the origin == destination
    if origin == destination:
        all_routes.append(route.copy())

    # Recursive Case    
    else:
        # Recursively calling the function for all the neighbors of the origin
        for neighbor in getOutgoingNeighbors(graph, origin):
            if neighbor not in route:
                all_routes = DFS_all_routes(graph, neighbor, destination, route, all_routes)
    
    # Backtracking to empty the route list
    route.pop()
    

    ## Iterative Approach (For round trips for the same origin and destination) ##

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
    
    # Initialization
    all_routes = []
    route = []

    # Checking if the origin is in the graph
    if origin not in graph:
        return None
    
    # Checking if the destination is in the graph
    if destination not in graph: 
        return None
    
    # Checking if the origin and the destination are the same and returns an empty list
    if destination == origin:
        return all_routes
        
    # Calling the DFS function to find all the routes
    all_routes = DFS_all_routes(graph, origin, destination, route, all_routes)
    
    return all_routes

def DFS_layovers(graph: dict, origin: str, destination: str, route: list, layovers_lst: list):
    
    # Starting from the origin
    route.append(origin)

    # Base Case - appends the length of the route list - 2(done for origin and destination)
    if origin == destination:
        layovers_lst.append(len(route) - 2)

    # Recursive Case  
    else:
        # Recursively calling the function for all the neighbors of the origin
        for neighbor in getOutgoingNeighbors(graph, origin):
            if neighbor not in route:
                layovers_lst = DFS_layovers(graph, neighbor, destination, route, layovers_lst)
    
    # Backtracking to empty the route list
    route.pop()

    return layovers_lst

def find_number_of_layovers(graph: dict, origin: str, destination: str):
    
    # Initialization
    layovers_lst = []
    route = []
    
    # Checking if the origin is in the graph
    if origin not in graph:
        return None
    
    # Checking if the destination is in the graph
    if destination not in graph: 
        return None
    
    # Checking if the origin and the destination are the same and returns an empty list
    if destination == origin:
        return layovers_lst
    
    # Calling the DFS function to find the number of layovers for each route
    layovers_lst = DFS_layovers(graph, origin, destination, route, layovers_lst)
    
    # Applying Selection Sort to sort the list (.sort() was not working for some reason)
    for i in range(len(layovers_lst)):
        min = i
        for j in range(i+1, len(layovers_lst)):
            if layovers_lst[j] < layovers_lst[min]:
                min = j
        layovers_lst[i], layovers_lst[min] = layovers_lst[min], layovers_lst[i]
    
    return layovers_lst

def main(): # For testing purposes

    option = 2
    filename = 'flight_network.csv'
    G = create_flight_network(filename, option)
    print(G)

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