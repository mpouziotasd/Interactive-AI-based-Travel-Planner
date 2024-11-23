import streamlit as st


# Beautified Using ChatGPT4o
def make_interface(graph_distances, graph_cost):
    """
        SIDEBAR UI
    """
    st.sidebar.header("Plan Your Travel ✈️")
    cities_labels = list(graph_distances.cities.keys())
    selected_city_departure = st.sidebar.selectbox(
        "Select Departure City:",
        options=cities_labels,
        index=cities_labels.index('Athens')
    )
    selected_city_destination = st.sidebar.selectbox(
        "Select Destination City:",
        options=cities_labels,
        index=cities_labels.index('Washington DC')
    )

    select_weight_bias = st.sidebar.selectbox(
        "Search By:",
        options=['Duration', 'Cost']
    )
    metric_duration = "Duration (hours): "
    metric_cost = "Cost (€): "
    if select_weight_bias == 'Cost':
        distances, paths = graph_cost.djikstra(selected_city_departure)
        destination_value = distances[graph_cost.cities[selected_city_destination][1]]
        routes = paths[selected_city_destination]
        graph_cost.make_destination_info(selected_city_destination)

        route_methods = list(dict.fromkeys(graph_cost.get_travel_methods()))
        value = graph_cost.get_duration()

        duration_str = metric_duration + str(value)
        cost__str = metric_cost + str(destination_value)

    elif select_weight_bias == 'Duration':
        distances, paths = graph_distances.djikstra(selected_city_departure)
        destination_value = distances[graph_distances.cities[selected_city_destination][1]]
        routes = paths[selected_city_destination]
        graph_distances.make_destination_info(selected_city_destination)

        route_methods = list(dict.fromkeys(graph_distances.get_travel_methods()))
        value = graph_distances.get_cost()

        duration_str = metric_duration + str(destination_value)
        cost__str = metric_cost + str(value)
    print
    """ 
        TICKET LAYOUT 
    """
    st.markdown("<h2 style='text-align: center;'>Your Travel Ticket 🎟️</h2>", unsafe_allow_html=True)

    st.write("---")
    route_methods = " and ".join(route_methods)
    formatted_route_methods = "By " + route_methods
    st.markdown(f"""
                <div style='border: 2px solid #4CAF50; border-radius: 15px; padding: 15px; background-color: #f9f9f9; color: #000000;'>
                    <h3 style='text-align: center; color: #000000;'>From: <b>{selected_city_departure}</b></h3>
                    <h3 style='text-align: center; color: #000000;'>To: <b>{selected_city_destination}</b></h3>
                    <p style='text-align: center; font-size: 16px; color: #000000;'>
                        <b>Search Preference:</b> {select_weight_bias}<br>
                        <b>{cost__str}</b> <br>
                        <b>{duration_str}</b> <br>
                        <b>Total Hops:</b> {len(routes) - 1} {formatted_route_methods} <br>
                    </p>
                </div>
                """, 
                unsafe_allow_html=True)

    st.write("✈️ Travel smart with our easy route finder!")
    st.write("---")

    selections = {"Destination": selected_city_destination, 
                  "Departure": selected_city_departure,
                  "Option": select_weight_bias}
    
    return selections, routes

import pydeck as pdk
from geopy.distance import geodesic


# Generated but not revised using ChatGPT4o
def make_gis(graph_distances, selections, routes):
    coordinates = [
        (graph_distances.cities[city][0].latitude, graph_distances.cities[city][0].longitude)
        for city in routes
    ]

    # Generate geodesic path data for each hop
    geodesic_path_data = []
    for i in range(len(coordinates) - 1):
        start_coords = coordinates[i]
        end_coords = coordinates[i + 1]
        
        # Generate geodesic eliptical points between hops
        geodesic_points = calculate_geodesic_points(start_coords, end_coords, n_points=50)

        # Convert to geodesic path segments
        for j in range(len(geodesic_points) - 1):
            geodesic_path_data.append({
                "source_position": [geodesic_points[j][0], geodesic_points[j][1]],  # lon, lat
                "target_position": [geodesic_points[j + 1][0], geodesic_points[j + 1][1]],  # lon, lat
            })

    # Create LineLayer for each hops
    line_layer = pdk.Layer(
        "LineLayer",
        data=geodesic_path_data,
        get_source_position="source_position",
        get_target_position="target_position",
        get_color="[255, 0, 0]", # [R, G, B]: Red
        get_width=2,
    )

    # Add markers for all cities in the route
    markers_data = [{"lat": coords[0], "lon": coords[1]} for coords in coordinates]
    marker_layer = pdk.Layer(
        "ScatterplotLayer",
        data=markers_data,
        get_position="[lon, lat]",
        get_color="[0, 0, 255]",  # [R, G, B]: Blue
        get_radius=50000,
    )

    # Map View Configuration
    mid_latitude = sum(coords[0] for coords in coordinates) / len(coordinates)
    mid_longitude = sum(coords[1] for coords in coordinates) / len(coordinates)
    total_distance_km = geodesic(coordinates[0], coordinates[-1]).kilometers
    dynamic_zoom = calculate_dynamic_zoom(total_distance_km)

    # Map Box Creation
    view_state = pdk.ViewState(
        latitude=mid_latitude,
        longitude=mid_longitude,
        zoom=dynamic_zoom,    # Dynamic Zoom Adjustment
        pitch=45,  # Tilt for a 3D map box effect
    )

    # Max Box Rendering with Streamlit
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/satellite-streets-v11",  # Satellite style map box
        initial_view_state=view_state,
        layers=[line_layer, marker_layer],
    ))




from pyproj import Geod

# Generated using ChatGPT4o
def calculate_geodesic_points(start_coords, end_coords, n_points=100):
    geod = Geod(ellps="WGS84")  # Use WGS84 ellipsoid to simulate Earth's spherical shape
    intermediate_points = geod.npts(
        start_coords[1], start_coords[0],  # Start longitude, latitude
        end_coords[1], end_coords[0],      # End longitude, latitude
        n_points - 2                       # Number of intermediate points (excluding start and end)
    )
    points = [(start_coords[1], start_coords[0])] + intermediate_points + [(end_coords[1], end_coords[0])]

    return points


import numpy as np

# Generated/Revised using ChatGPT4o
def calculate_dynamic_zoom(distance_km, max_zoom=10, min_zoom=2, zoom_factor=2):
    distance_km = max(distance_km, 1)
    zoom = max_zoom - (np.log10(distance_km) * zoom_factor)
    return max(min(zoom, max_zoom), min_zoom)