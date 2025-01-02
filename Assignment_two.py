import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import heapq


def uninformed_path_finder(cities, roads, start_city, goal_city, strategy):

    def bfs(start, goal):
        queue = deque([(start, [start])])
        visited = set([start])

        while queue:
            city, path = queue.popleft()
            if city == goal:
                return path, len(path) - 1
            for neighbor, _ in roads.get(city, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return None, None

    def dfs(start, goal):
        stack = [(start, [start])]
        visited = set([start])
        while stack:
            city, path = stack.pop()
            if city == goal:
                return path, len(path) - 1
            for neighbor, _ in roads.get(city, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append((neighbor, path + [neighbor]))

        return None, None
    def bfs_weighted(start, goal):
        pq = [(0, start, [start])]
        visited = set([start])

        while pq:
            cost, city, path = heapq.heappop(pq)
            if city == goal:
                return path, cost
            for neighbor, distance in roads.get(city, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    heapq.heappush(pq, (cost + distance, neighbor, path + [neighbor]))
        return None, None

    if strategy == 'bfs':
        return bfs(start_city, goal_city)
    elif strategy == 'dfs':
        return dfs(start_city, goal_city)
    elif strategy == 'bfs_weighted':
        return bfs_weighted(start_city, goal_city)
    else:
        return None, None  # Invalid strategy
cities = ['Addis Ababa', 'Bahir Dar', 'Gondar', 'Hawassa', 'Mekelle']
roads = {
    'Addis Ababa': [('Bahir Dar', 510), ('Hawassa', 275)],
    'Bahir Dar': [('Addis Ababa', 510), ('Gondar', 180)],
    'Gondar': [('Bahir Dar', 180), ('Mekelle', 300)],
    'Hawassa': [('Addis Ababa', 275)],
    'Mekelle': [('Gondar', 300)]
}

start = 'Addis Ababa'
goal = 'Mekelle'
strategy = 'bfs'
path, cost = uninformed_path_finder(cities, roads, start, goal, strategy)
print(f"Path: {path}, Cost: {cost}")


def uninformed_path_finder(cities, roads, start_city, goal_city, strategy):

    def bfs(start, goal):
        queue = deque([(start, [start])])
        visited = set([start])
        while queue:
            city, path = queue.popleft()
            if city == goal:
                return path, len(path) - 1
            for neighbor, _ in roads.get(city, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return None, None

    def dfs(start, goal):
        stack = [(start, [start])]
        visited = set([start])
        while stack:
            city, path = stack.pop()
            if city == goal:
                return path, len(path) - 1
            for neighbor, _ in roads.get(city, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append((neighbor, path + [neighbor]))
        return None, None
    def bfs_weighted(start, goal):
        pq = [(0, start, [start])]
        visited = set([start])

        while pq:
            cost, city, path = heapq.heappop(pq)
            if city == goal:
                return path, cost
            for neighbor, distance in roads.get(city, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    heapq.heappush(pq, (cost + distance, neighbor, path + [neighbor]))
        return None, None
    if strategy == 'bfs':
        return bfs(start_city, goal_city)

    elif strategy == 'dfs':
        return dfs(start_city, goal_city)
    elif strategy == 'bfs_weighted':
        return bfs_weighted(start_city, goal_city)
    else:
        return None, None
def traverse_all_cities(cities, roads, start_city, strategy):
    path = [start_city]
    total_cost = 0
    cities_left = set(cities) - {start_city}
    current_city = start_city
    while cities_left:
        for city in cities_left:
            sub_path, sub_cost = uninformed_path_finder(cities, roads, current_city, city, strategy)
            if sub_path:
                path.extend(sub_path[1:])
                total_cost += sub_cost
                cities_left -= set(sub_path)
                current_city = sub_path[-1]
                break
    return path, total_cost
def visualize_road_network(cities, roads, path=None):
    G = nx.Graph()
    for city, neighbors in roads.items():
        for neighbor, distance in neighbors:
            G.add_edge(city, neighbor, weight=distance)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=12)
    if path:
        edges_in_path = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=edges_in_path, edge_color='red', width=3)
    plt.show()
cities = ['Addis Ababa', 'Bahir Dar', 'Gondar', 'Hawassa', 'Mekelle']
roads = {
    'Addis Ababa': [('Bahir Dar', 510), ('Hawassa', 275)],
    'Bahir Dar': [('Addis Ababa', 510), ('Gondar', 180)],
    'Gondar': [('Bahir Dar', 180), ('Mekelle', 300)],
    'Hawassa': [('Addis Ababa', 275)],
    'Mekelle': [('Gondar', 300)]
}
start = 'Addis Ababa'
goal = 'Mekelle'
strategy = 'bfs'
path, cost = uninformed_path_finder(cities, roads, start, goal, strategy)
print(f"BFS Path: {path}, Cost: {cost}")
strategy = 'bfs'
traverse_path, traverse_cost = traverse_all_cities(cities, roads, start, strategy)
print(f"Travel All Cities Path: {traverse_path}, Total Cost: {traverse_cost}")
visualize_road_network(cities, roads, traverse_path)
