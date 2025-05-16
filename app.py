from flask import Flask, render_template, request, jsonify
import folium
import networkx as nx
from shapely.geometry import Point, Polygon

app = Flask(__name__)

# Simulated flood/accident areas as polygons (latitude, longitude)
DISASTER_AREAS = [
    Polygon([(37.78, -122.42), (37.79, -122.42), (37.79, -122.41), (37.78, -122.41)]),  # Example polygon
    Polygon([(37.77, -122.43), (37.775, -122.43), (37.775, -122.425), (37.77, -122.425)]),
]

# Create a simple grid graph for pathfinding
def create_graph():
    G = nx.grid_2d_graph(100, 100)  # 100x100 grid
    # Remove nodes inside disaster areas
    nodes_to_remove = []
    for node in G.nodes:
        lat = 37.70 + (node[0] * 0.001)  # scale to lat range approx
        lon = -122.50 + (node[1] * 0.001)  # scale to lon range approx
        point = Point(lat, lon)
        for area in DISASTER_AREAS:
            if area.contains(point):
                nodes_to_remove.append(node)
                break
    G.remove_nodes_from(nodes_to_remove)
    return G

GRAPH = create_graph()

def latlon_to_node(lat, lon):
    x = int((lat - 37.70) / 0.001)
    y = int((lon + 122.50) / 0.001)
    return (x, y)

def node_to_latlon(node):
    lat = 37.70 + (node[0] * 0.001)
    lon = -122.50 + (node[1] * 0.001)
    return (lat, lon)

@app.route('/')
def index():
    start = (37.70, -122.50)
    end = (37.79, -122.40)
    m = folium.Map(location=[(start[0]+end[0])/2, (start[1]+end[1])/2], zoom_start=13)

    # Add disaster areas to map as red rectangles with interactivity
    for area in DISASTER_AREAS:
        bounds = [(p[0], p[1]) for p in area.exterior.coords]
        # folium.Rectangle expects bounds as two points: southwest and northeast corners
        # Calculate southwest and northeast corners from polygon coords
        lats = [p[0] for p in area.exterior.coords]
        lons = [p[1] for p in area.exterior.coords]
        sw = (min(lats), min(lons))
        ne = (max(lats), max(lons))
        folium.Rectangle(bounds=[sw, ne], color='red', fill=True, fill_opacity=0.5,
                         popup='Accident Zone',
                         tooltip='Accident Zone - Click for info').add_to(m)

    # Add start and end markers
    folium.Marker(location=start, popup='Start', icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(location=end, popup='End', icon=folium.Icon(color='blue')).add_to(m)

    # Render map to HTML
    map_html = m._repr_html_()
    return render_template('index.html', map_html=map_html)

@app.route('/find_path', methods=['POST'])
def find_path():
    data = request.json
    start_lat = float(data['start_lat'])
    start_lon = float(data['start_lon'])
    end_lat = float(data['end_lat'])
    end_lon = float(data['end_lon'])

    start_node = latlon_to_node(start_lat, start_lon)
    end_node = latlon_to_node(end_lat, end_lon)

    try:
        path_nodes = nx.shortest_path(GRAPH, source=start_node, target=end_node)
        path_coords = [node_to_latlon(node) for node in path_nodes]
        return jsonify({'path': path_coords})
    except nx.NetworkXNoPath:
        return jsonify({'error': 'No path found avoiding disaster areas'}), 400

if __name__ == '__main__':
    app.run(debug=True)
