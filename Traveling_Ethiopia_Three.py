from random import random
import time
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import heapq


class AStarSearchVisualizer:
    def __init__(self, roads):
        self.roads = roads
        self.graph = self.create_graph()

    def create_graph(self):
        # Create a directed graph using NetworkX
        G = nx.Graph()
        for city, data in self.roads.items():
            for neighbor, distance in data['neighbors']:
                G.add_edge(city, neighbor, weight=distance)
        return G

    def heuristic(self, city):
        # Return the heuristic (straight-line distance to the goal)
        return self.roads[city]['cost']

    def a_star_search(self, start, goal):
        # Priority queue for the open set (cities to explore)
        open_set = []
        heapq.heappush(open_set, (0 + self.heuristic(start), start))

        # Dictionary to store the cost of reaching each city
        g_costs = {start: 0}

        # Dictionary to store the path taken
        came_from = {}

        while open_set:
            # Get the city with the lowest f-cost (g + h)
            current_f_cost, current_city = heapq.heappop(open_set)

            if current_city == goal:
                return self.reconstruct_path(came_from, current_city)

            for neighbor, distance in self.roads[current_city]['neighbors']:
                tentative_g_cost = g_costs[current_city] + distance

                if neighbor not in g_costs or tentative_g_cost < g_costs[neighbor]:
                    g_costs[neighbor] = tentative_g_cost
                    f_cost = tentative_g_cost + self.heuristic(neighbor)
                    heapq.heappush(open_set, (f_cost, neighbor))
                    came_from[neighbor] = current_city

        return None  # No path found

    def reconstruct_path(self, came_from, current):
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.append(current)
        path.reverse()
        return path

    def visualize(self, path):
        # Draw the graph
        pos = nx.spring_layout(self.graph, seed=49)  # Position nodes in a circular layout
        plt.figure(figsize=(15, 10))

        # Draw all nodes and edges
        nx.draw(self.graph, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=10)

        # Highlight the path
        path_edges = [(path[i], path[i+1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(self.graph, pos, edgelist=path_edges, edge_color='red', width=2)
        nx.draw_networkx_nodes(self.graph, pos, nodelist=path, node_color='orange')

        # Add labels to the edges
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)

        plt.title("A* Search Path Visualization", fontsize=15)
        plt.show()


roads = {
    'Kartum': { 'cost': 81, 'neighbors': [('Humera', 21), ('Metema', 19)] },
    'Humera': {'cost': 65, 'neighbors': [('Shire', 8), ('Gondar', 9)]},
    'Shire': {'cost': 67, 'neighbors': [('Axum', 2), ('Debarke', 7), ('Humera', 8)]},
    'Axum': {'cost': 66, 'neighbors': [('Shire', 2), ('Asmera', 5), ('Adwa', 1)]},
    'Asmera': {'cost': 68, 'neighbors': [('Axum', 5), ('Adigrat', 9)]},
    'Adigrat': {'cost': 62, 'neighbors': [('Adwa', 4), ('Mekelle', 4), ('Asmera', 9)]},
    'Metema': {'cost': 62, 'neighbors': [('Kartum', 19), ('Gondar', 7), ('Azezo', 7)]},
    'Debarke': {'cost': 60, 'neighbors': [('Gondar', 4), ('Shire', 7)]},
    'Adwa': {'cost': 65, 'neighbors': [('Axum', 1), ('Adigrat', 4), ('Mekelle', 7)]},
    'Mekelle': {'cost': 58, 'neighbors': [('Adwa', 7), ('Adigrat', 4), ('Sekota', 9), ('Alamata', 5)]},
    'Gondar': {'cost': 56, 'neighbors': [('Debarke', 4), ('Metema', 7), ('Azezo', 1), ('Debre Tabor', 6)]},
    'Bahir Dar': {'cost': 48, 'neighbors': [('Azezo', 7), ('Debre Tabor', 4), ('Metekel', 11), ('Injibara', 4), ('Finote Selam', 6)]},
    'Azezo': {'cost': 55, 'neighbors': [('Gondar', 1), ('Metema', 7), ('Bahir Dar', 7)]},
    'Debre Tabor': {'cost': 52, 'neighbors': [('Bahir Dar', 4), ('Gondar', 6), ('Lalibela', 8)]},
    'Lalibela': {'cost': 57, 'neighbors': [('Debre Tabor', 8), ('Sekota', 6), ('Woldia', 7)]},
    'Sekota': {'cost': 59, 'neighbors': [('Mekelle', 9), ('Alamata', 6), ('Lalibela', 7)]},
    'Alamata': {'cost': 53, 'neighbors': [('Sekota', 6), ('Mekele', 5), ('Samara', 11), ('Woldia', 3)]},
    'Woldia': {'cost': 50, 'neighbors': [('Dessie', 6), ('Alamata', 3), ('Lalibela', 7), ('Samara', 8)]},
    'Kilbet Rasu': {'cost': 55, 'neighbors': [('Fanti Rasu', 6)]},
    'Fanti Rasu': {'cost': 49, 'neighbors': [('Samara', 7), ('Kilbet Rasu', 6)]},
    'Samara': {'cost': 42, 'neighbors': [('Fanti Rasu', 7), ('Alamata', 11), ('Woldia', 8), ('Gabi Rasu', 10)]},
    'Dessie': {'cost': 44, 'neighbors': [('Woldia', 6), ('Kemise', 4)]},
    'Kemise': {'cost': 40, 'neighbors': [('Debre Sina', 6), ('Dessie', 4)]},
    'Debre Sina': {'cost': 33, 'neighbors': [('Kemise', 7), ('Debre Birhan', 2), ('Debre Markos', 17)]},
    'Metekel': {'cost': 59, 'neighbors': [('Bahir Dar', 11)]},
    'Injibara': {'cost': 44, 'neighbors': [('Bahir Dar', 4), ('Finote Selam', 2)]},
    'Finote Selam': {'cost': 42, 'neighbors': [('Bahir Dar', 6), ('Injibara', 2), ('Debre Markos', 3)]},
    'Debre Markos': {'cost': 39, 'neighbors': [('Finote Selam', 3), ('Debre Sina', 17), ('Debre Sina', 17)]},
    'Gabi Rasu': {'cost': 32, 'neighbors': [('Samara', 9), ('Awash', 0)]},
    'Awash': {'cost': 27, 'neighbors': [('Matahara', 1), ('Chiro', 4), ('Addis Ababa', 13)]},
    'Chiro': {'cost': 31, 'neighbors': [('Awash', 4), ('Dire Dawa', 8)]},
    'Dire Dawa': {'cost': 31, 'neighbors': [('Chiro', 8), ('Harar', 4)]},
    'Harar': {'cost': 35, 'neighbors': [('Dire Dawa', 4), ('Babile', 2)]},
    'Babile': {'cost': 37, 'neighbors': [('Harar', 2), ('Jigjiga', 3), ('Goba', 28)]},
    'Jigjiga': {'cost': 40, 'neighbors': [('Babile', 3), ('Dega Habur', 5)]},
    'Dega Habur': {'cost': 45, 'neighbors': [('Jigjiga', 5), ('Kebri Dehar', 6)]},
    'Assosa': {'cost': 51, 'neighbors': [('Dembi Dollo', 12), ('Gimbi', 8)]},
    'Dembi Dollo': {'cost': 49, 'neighbors': [('Assosa', 12), ('Gimbi', 6), ('Gambella', 4)]},
    'Gimbi': {'cost': 43, 'neighbors': [('Assosa', 8), ('Dembi Dollo', 6), ('Nekemte', 4)]},
    'Nekemte': {'cost': 39, 'neighbors': [('Gimbi', 4), ('Ambo', 8), ('Bedelle', 4)]},
    'Ambo': {'cost': 31, 'neighbors': [('Nekemte', 8), ('Addis Ababa', 5), ('Wolkite', 6)]},
    'Gambella': {'cost': 51, 'neighbors': [('Dembi Dollo', 4), ('Gore', 5)]},
    'Gore': {'cost': 46, 'neighbors': [('Gambella', 5), ('Bedelle', 6), ('Tepi', 9)]},
    'Tepi': {'cost': 41, 'neighbors': [('Gore', 9), ('Mezan Teferi', 4), ('Bonga', 8)]},
    'Bonga': {'cost': 33, 'neighbors': [('Tepi', 8), ('Mezan Teferi', 4), ('Jimma', 4), ('Dawro', 10)]},
    'Mezan Teferi': {'cost': 37, 'neighbors': [('Tepi', 4), ('Bonga', 4)]},
    'Jimma': {'cost': 33, 'neighbors': [('Bonga', 4), ('Bedelle', 7), ('Wolkite', 8)]},
    'Bedelle': {'cost': 40, 'neighbors': [('Jimma', 7), ('Gore', 6), ('Nekemte', 4)]},
    'Wolkite': {'cost': 25, 'neighbors': [('Ambo', 6), ('Jimma', 8), ('Worabe', 5), ('Hossana', 5), ('Buta Jirra', 4)]},
    'Buta Jirra': {'cost': 21, 'neighbors': [('Worabe', 2), ('Batu', 2), ('Wolkite', 5)]},
    'Batu': {'cost': 19, 'neighbors': [('Buta Jirra', 2), ('Adama', 4), ('Shashemene', 3)]},
    'Adama': {'cost': 23, 'neighbors': [('Batu', 4), ('Matahara', 3), ('Asella', 4), ('Addis Ababa', 3)]},
    'Matahara': {'cost': 26, 'neighbors': [('Awash', 1), ('Adama', 3)]},
    'Addis Ababa': {'cost': 26, 'neighbors': [('Ambo', 5), ('Adama', 3), ('Debre Birhan', 5), ('Debre Markos', 13)]},
    'Debre Birhan': {'cost': 31, 'neighbors': [('Addis Ababa', 5), ('Debre Sina', 2)]},
    'Dawro': {'cost': 23, 'neighbors': [('Wolaita Sodo', 6), ('Bonga', 10)]},
    'Wolaita Sodo': {'cost': 17, 'neighbors': [('Dawro', 6), ('Hossana', 4), ('Arba Minch', 4)]},
    'Hossana': {'cost': 21, 'neighbors': [('Wolaita Sodo', 4), ('Worabe', 2), ('Shashemene', 7), ('Wolkite', 5)]},
    'Worabe': {'cost': 22, 'neighbors': [('Wolkite', 5), ('Buta Jirra', 2), ('Hossana', 2), ('Shashemene', 6)]},
    'Shashemene': {'cost': 16, 'neighbors': [('Batu', 3), ('Hossana', 7), ('Hawassa', 1), ('Dodolla', 3)]},
    'Assasa': {'cost': 18, 'neighbors': [('Asella', 4), ('Dodolla', 1)]},
    'Dodolla': {'cost': 19, 'neighbors': [('Robe', 13), ('Assasa', 1), ('Shashemene', 3)]},
    'Robe': {'cost': 22, 'neighbors': [('Goba', 18), ('Dodolla', 13), ('Sof Oumer', 23), ('Liben', 11)]},
    'Goba': {'cost': 40, 'neighbors': [('Babile', 28), ('Sof Oumer', 6), ('Robe', 18)]},
    'Sof Oumer': {'cost': 45, 'neighbors': [('Goba', 6), ('Robe', 23), ('Gode', 23)]},
    'Kebri Dehar': {'cost': 40, 'neighbors': [('Weder', 6), ('Gode', 5), ('Dega Habur', 6)]},
    'Weder': {'cost': 46, 'neighbors': [('Kebri Dehar', 6)]},
    'Gode': {'cost': 35, 'neighbors': [('Dollo', 17), ('Kebri Dehar', 5), ('Mokadisho', 22), ('Sof Oumer', 23)]},
    'Bench Maji': {'cost': 28, 'neighbors': [('Juba', 22), ('Basketo', 23)]},
    'Basketo': {'cost': 23, 'neighbors': [('Benchi Maji', 5), ('Arba Minch', 10)]},
    'Arba Minch': {'cost': 13, 'neighbors': [('Wolaita Sodo', 4), ('Konso', 4), ('Basketo', 10)]},
    'Konso': {'cost': 9, 'neighbors': [('Arba Minch', 4), ('Yabello', 3)]},
    'Hawassa': {'cost': 15, 'neighbors': [('Shashemene', 1), ('Dilla', 3)]},
    'Dilla': {'cost': 12, 'neighbors': [('Hawassa', 3), ('Bule Hora', 4)]},
    'Bule Hora': {'cost': 8, 'neighbors': [('Dilla', 4), ('Yabello', 2)]},
    'Yabello': {'cost': 6, 'neighbors': [('Bule Hora', 2), ('Moyale', 6), ('Konso', 3)]},
    'Moyale': {'cost': 0, 'neighbors': [('Yabello', 6), ('Nairobi', 22), ('Liben', 11), ('Dollo', 18), ('Mokadisho', 40)]},
    'Liben': {'cost': 11, 'neighbors': [('Moyale', 11), ('Robe', 11)]},
    'Dollo': {'cost': 18, 'neighbors': [('Gode', 17), ('Bale', 18)]},
    'Asella': {'cost': 22, 'neighbors': [('Assasa', 4), ('Adama', 4)]},
    'Werder': {'cost': 46, 'neighbors': [('Kebri Dehar', 6)]},
    'Juba': {'cost': 50, 'neighbors': [('Bench Maji', 22)]},
    'Mokadisho': {'cost': 40, 'neighbors': [('Gode', 22), ('Moyale', 40)]},
    'Nairobi': {'cost': 22, 'neighbors': [('Moyale', 22)]},
}


# Instantiate and test the A* search with visualization
search_visualizer = AStarSearchVisualizer(roads)
start_city = "Addis Ababa"
goal_city = "Moyale"

path = search_visualizer.a_star_search(start_city, goal_city)
if path:
    print("Optimal path:", " -> ".join(path))
    search_visualizer.visualize(path)
else:
    print("No path found between the specified cities.")
