import heapq
from flask import Flask, request, jsonify

def dijkstra(graph, start):
    shortest_path = {}
    unvisited = graph
    infinity = float('inf')
    path = {}
    shortest_path[start] = 0
    while unvisited:
        current_vertex = None
        for vertex in unvisited:
            if vertex in shortest_path:
                if current_vertex is None:
                    current_vertex = vertex
                elif shortest_path[vertex] < shortest_path[current_vertex]:
                    current_vertex = vertex
        if shortest_path[current_vertex] == infinity:
            break
        neighbors = graph[current_vertex].items()
        for neighbor, weight in neighbors:
            if neighbor not in shortest_path:
                new_distance = shortest_path[current_vertex] + weight
                if new_distance < shortest_path.get(neighbor, infinity):
                    shortest_path[neighbor] = new_distance
                    path[neighbor] = current_vertex
        unvisited.pop(current_vertex)
    return shortest_path, path

def shortest_path(graph, origin, destination):
    shortest_distance, paths = dijkstra(graph, origin)
    route = [destination]
    while destination in paths:
        route.append(paths[destination])
        destination = paths[destination]
    route.reverse()
    return route


app = Flask(__name__)

@app.route('/shortest_path/', methods=['GET'])
def find_shortest_path():
    # Example graph for demonstration purposes
    graph = {
        'A': {'B': 1, 'D': 3},
        'B': {'A': 1, 'D': 2, 'E': 5},
        'D': {'A': 3, 'B': 2, 'E': 1},
        'E': {'B': 5, 'D': 1},
    }

    origin = request.args.get('origin')
    destination = request.args.get('destination')
    
    if origin not in graph or destination not in graph:
        return "Invalid input", 400

    path = shortest_path(graph, origin, destination)
    return jsonify(path)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
