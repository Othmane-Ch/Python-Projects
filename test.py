from math import sqrt
import heapq
import folium

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = {}
        self.distances = {}

    def add_node(self, value):
        self.nodes.add(value)
        self.edges[value] = []

    def add_edge(self, from_node, to_node, distance):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.distances[(from_node, to_node)] = distance
        self.distances[(to_node, from_node)] = distance

    def dijkstra_algorithm(self, initial_node, end_node):
        distances = {node: float('infinity') for node in self.nodes}
        distances[initial_node] = 0

        queue = []
        heapq.heappush(queue, [distances[initial_node], initial_node])

        while queue:
            current_distance, current_node = heapq.heappop(queue)

            if current_node == end_node:
                path = []
                while current_node in previous_nodes:
                    path.append(current_node)
                    current_node = previous_nodes[current_node]
                return path[::-1]

            for neighbor in self.edges[current_node]:
                distance = self.distances[(current_node, neighbor)]
                tentative_distance = distances[current_node] + distance
                if tentative_distance < distances[neighbor]:
                    distances[neighbor] = tentative_distance
                    heapq.heappush(queue, [tentative_distance, neighbor])
                    previous_nodes[neighbor] = current_node

        return -1

    def a_star_algorithm(self, initial_node, end_node):
        def heuristic(node):
            x1, y1 = node
            x2, y2 = end_node
            return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        open_list = set()
        closed_list = set()
        g = {}
        f = {}

        g[initial_node] = 0
        f[initial_node] = heuristic(initial_node)
        open_list.add(initial_node)

        while open_list:
            current_node = None
            current_f_score = None
            for node in open_list:
                if current_node is None or f[node] < current_f_score:
                    current_f_score = f[node]
                    current_node = node

            if current_node == end_node:
                path = []
                while current_node in previous_nodes:
                    path.append(current_node)
                    current_node = previous_nodes[current_node]
                return path[::-1]

            open_list.remove(current_node)
            closed_list.add(current_node)

            for neighbor in self.edges[current_node]:
                if neighbor in closed_list:
                    continue
                tentative_g_score = g[current_node] + self.distances[(current_node, neighbor)]
                if neighbor not in open_list:
                    open_list.add(neighbor)
                elif tentative_g_score >= g[neighbor]:
                    continue

                previous_nodes[neighbor] = current_node
                g[neighbor] = tentative_g_score
                h = heuristic(neighbor)
                f[neighbor] = g[neighbor] + h

        return -1

graph = Graph()
graph.add_node((0, 0))
graph.add_node((1, 1))
graph.add_node((2, 2))
graph.add_node((3, 3))
graph.add_node((4, 4))

graph.add_edge((0, 0), (1, 1), 1.5)
graph.add_edge((1, 1), (2, 2), 2.5)
graph.add_edge((2, 2), (3, 3), 3.5)
graph.add_edge((3, 3), (4, 4), 4.5)

previous_nodes = {}

path = graph.a_star_algorithm((0, 0), (4, 4))

if path != -1:
print("Shortest path found:", path)
else:
print("No path found")

m = folium.Map(location=[2, 2], zoom_start=2)
folium.PolyLine(locations=path).add_to(m)
m.save('path.html')
