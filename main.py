from utils.load_data import load_data
from src.djikstra import Graph, City


# Load Data
cities_data_src = load_data('data/cities.csv',
                            dtypes={"Country": str, 'City': str, 'Latitude': float, 'Longitude': float})

routes_data_src = load_data('data/routes.csv',
                            dtypes={'Departure': str, 'Destination': str, 'Transportation Method': str,
                                    'Duration': float, 'Cost': float, 'Description': str})

# Graph Initialization
graph_distances = Graph(cities_count=len(cities_data_src))
graph_cost = Graph(cities_count=len(cities_data_src))

# Graph Vertex Population
for index, row in cities_data_src.iterrows():
    _city = row["City"]
    _country = row["Country"]
    _lat, _lon = row['Latitude'], row['Longitude']
    city = City(_city, _country, _lat, _lon)
    graph_distances.add_vertex_data(index, city)
    graph_cost.add_vertex_data(index, city)

# Routes Population (Adjacency Matrix Population)
for index, row in routes_data_src.iterrows():
    departure = row["Departure"]
    destination = row["Destination"]
    duration = row["Duration"]
    cost = row["Cost"]
    method = row['Transportation Method']

    departure_index = graph_distances.cities[departure][1]
    destination_index = graph_distances.cities[destination][1]

    graph_distances.add_route(departure_index, destination_index, 
                            duration, 
                            method,
                            cost, duration)
                            
    graph_cost.add_route(departure_index, destination_index, 
                         cost, 
                         method,
                         cost, duration)


"""
    User Interface with Streamlit
"""
from src.streamlit_interface import make_interface, make_gis

# Returns User Inputs from Interface
selections, routes = make_interface(graph_distances, graph_cost) 

"""
    Route Visualization using GIS
"""
make_gis(graph_distances, selections, routes)

