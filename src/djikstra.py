class City:
    def __init__(self, city, country, lat, lon):
        self.city_name = city
        self.country = country
        self.latitude = lat
        self.longitude = lon

class Graph:
    def __init__(self, cities_count):
        self.total_cities = cities_count
        self.cities = {}
        self.adj_matrix = [[0.0] * cities_count for _ in range(cities_count)]  # Standard weights
        self.distances = None # Distance for every 

        self.routes = None
        
        self.cost_matrix = [[None] * cities_count for _ in range(cities_count)]
        self.route_method_matrix = [[None] * cities_count for _ in range(cities_count)]
        self.duration_matrix = [[None] * cities_count for _ in range(cities_count)]
        self.previous_flights = None
        self.total_route_cost = None
        self.total_route_duration = None
        self.travel_methods = None


    def add_route(self, src_index, dst_index, weight, travel_method, cost, duration):
        if src_index < self.total_cities and dst_index < self.total_cities:
            self.adj_matrix[src_index][dst_index] = weight
            self.route_method_matrix[src_index][dst_index] = travel_method
            self.cost_matrix[src_index][dst_index] = cost
            self.duration_matrix[src_index][dst_index] = duration

    # https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/
    def add_vertex_data(self, vertex_index, city):
        if vertex_index < self.total_cities:
            self.cities[city.city_name] = (city, vertex_index)

    def get_minDistance_index(self, distances, visited):
        min_distance = float('inf') # Init Min Distance with Infinity
        min_index = None
        
        for i in range(self.total_cities):
            if not visited[i] and distances[i] < min_distance:
                min_distance = distances[i]
                min_index = i

        return min_index

    def djikstra(self, start_departure):
        _, start_index = self.cities[start_departure]  # Index of the Departuring city
        distances = [float('inf')] * self.total_cities # Init Distances of Cities with Infinity
        distances[start_index] = 0
        visited = [False] * self.total_cities

        predecessors = [None] * self.total_cities
        routes = {start_departure: [start_departure]}  # Initialize paths with the start city
        
        for _ in range(self.total_cities):
            u = self.get_minDistance_index(distances, visited)

            if u is None:
                break
            visited[u] = True
            for v in range(self.total_cities):
                if self.adj_matrix[u][v] != 0 and not visited[v]:
                    alt = distances[u] + self.adj_matrix[u][v]
                    if alt < distances[v]:
                        distances[v] = alt

                        # New:
                        predecessors[v] = u
                        current_city = self.get_city_name(v)
                        previous_city = self.get_city_name(u)
                        routes[current_city] = routes[previous_city] + [current_city]
                    
        self.distances = distances
        self.routes = routes

        return distances, routes

    def get_cost(self):
        return self.total_route_cost
    
    def get_duration(self):
        return self.total_route_duration
    def get_travel_methods(self):
        return self.travel_methods

    def make_destination_info(self, dest_name):
        routes = self.routes[dest_name]
        travel_methods = []
        total_route_cost = 0.0
        total_route_duration = 0.0
        for i in range(0, len(routes) - 1):
            _depart_index = self.cities[routes[i]][1] # Temp Departure Index
            _dest_index = self.cities[routes[i+1]][1] # Temp Destination Index
            travel_methods.append(self.route_method_matrix[_depart_index][_dest_index])
            total_route_cost += self.cost_matrix[_depart_index][_dest_index]
            total_route_duration += self.duration_matrix[_depart_index][_dest_index]

        self.total_route_cost = total_route_cost
        self.total_route_duration = total_route_duration
        self.travel_methods = travel_methods


    def get_route_methods(self, dest_name):
        routes = self.routes[dest_name]
        
        travel_methods = []
        for i in range(0, len(routes)-1):
            _depart_index = self.cities[routes[i]][1] # Temp Departure Index
            _dest_index = self.cities[routes[i+1]][1] # Temp Destination Index
            travel_methods.append(self.route_method_matrix[_depart_index][_dest_index])
        return travel_methods


    def get_city_name(self, city_index):
        for city_name, (_, index) in self.cities.items():
            if index == city_index:
                return city_name
        return None

    def printSolution(self, dist):
        for node in range(self.V):
            print(node, f'\t {dist[node]}')
