from random import random
import time
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import heapq

class TravelEthiopia:
    def __init__(self, cities, roads, start=None, goals=None, strategy=None):
        self.cities = cities
        self.roads = roads
        self.start = start
        self.goals = set(goals) if goals else set()
        self.order = []  # Stores the order of visited nodes for visualization

        # Build the graph for visualization
        self.G = nx.Graph()
        for city in roads:
            for neighbor, _ in roads[city]:
                self.G.add_edge(city, neighbor)

    def ucs(self, start, goal):
        visited = set()
        priority_queue = [(0, start, [start])]  # Priority queue stores (cost, current city, path)

        while priority_queue:
            cost, city, path = heapq.heappop(priority_queue)

            if city not in visited:
                visited.add(city)
                self.order.append(city)  # Add to visit order for visualization

                # Goal check
                if city == goal:
                    return path, cost

                # Add neighbors to the priority queue
                for neighbor, travel_cost in self.roads.get(city, []):
                    if neighbor not in visited:
                        heapq.heappush(priority_queue, (cost + travel_cost, neighbor, path + [neighbor]))

        return None, float('inf')  # Return None and infinite cost if goal is not found

    def multi_goal_ucs(self):
        current_city = self.start
        remaining_goals = set(self.goals)
        total_path = []
        total_cost = 0

        while remaining_goals:
            # Find the closest goal state from the current city
            closest_goal = None
            min_cost = float('inf')
            best_path = None

            for goal in remaining_goals:
                path, cost = self.ucs(current_city, goal)
                if cost < min_cost:
                    min_cost = cost
                    closest_goal = goal
                    best_path = path

            if closest_goal is None:
                raise ValueError("No path exists to remaining goals.")

            # Update the total path and cost
            total_path.extend(best_path if not total_path else best_path[1:])  # Avoid duplicate cities in the path
            total_cost += min_cost
            remaining_goals.remove(closest_goal)
            current_city = closest_goal

        return total_path, total_cost

    def visualize_search(self, pos, title):
        plt.figure(figsize=(10, 8))
        for i, node in enumerate(self.order, start=1):
            plt.clf()
            plt.title(f"{title} - Step {i}")
            # Highlight the current node (red for current, green for others)
            nx.draw(
                self.G,
                pos,
                with_labels=True,
                node_color=['r' if n == node else 'g' if n in self.goals else 'b' for n in self.G.nodes],
                node_size=100,
                font_size=10
            )
            plt.draw()
            plt.pause(0.5)  # Pause to show each step for 2 seconds

            # Stop visualization if the goal is reached
            if node in self.goals:
                break
        plt.show()

    def search(self):
        # Reset visit order for each search
        self.order = []

        # Run the multi-goal UCS
        title = "Multi-Goal Uniform Cost Search"
        total_path, total_cost = self.multi_goal_ucs()
        print(f"Total Path: {total_path}, Total Cost: {total_cost}")

        # Visualize the search process
        pos = nx.spring_layout(self.G, seed=42)
        self.visualize_search(pos, title)

        return total_path, total_cost


cities = [
    'Kartum', 'Asmera', 'Shire', 'Adigrat', 'Axum', 'Adwa', 'Debarke', 'Mekelle', 'Sekota', 'Metema', 'Gondar',
    'Kilbet Rasu', 'Fanti Rasu', 'Azezo', 'Debre Tabor', 'Alamata', 'Samara', 'Woldia', 'Lalibela', 'Metekel', 'Bahir Dar',
    'Finote Selam', 'Injibara', 'Debre Markos', 'Dessie', 'Kemise', 'Debre Sina', 'Gabi Rasu', 'Debre Birhan',
    'Assosa', 'Dembi Dollo', 'Gimbi', 'Nekemte', 'Ambo', 'Addis Ababa', 'Bedelle', 'Wolkite', 'Buta Jirra',
    'Adama', 'Matahara', 'Awash', 'Chiro', 'Dire Dawa', 'Harar', 'Babile', 'Jigjiga', 'Dega Habur',
    'Batu', 'Asella', 'Gambella', 'Gore', 'Jimma', 'Hossana', 'Worabe', 'Tepi', 'Bonga', 'Shashemene',
    'Assasa', 'Mezan Teferi', 'Dawro', 'Wolaita Sodo', 'Hawassa', 'Dodolla', 'Bale', 'Goba', 'Sof Oumer',
    'Kebri Dehar', 'Werder',
    'Juba', 'Bench Maji', 'Basketo', 'Arba Minch', 'Konso', 'Dilla', 'Bule Hora', 'Yabello', 'Moyale',
    'Liben', 'Gode', 'Dollo', 'Mokadisho',
    'Nairobi'
]
roads = {
    'Kartum': [('Humera', 21), ('Metema', 19)],
    'Humera': [('Shire', 8), ('Gondar', 9)],
    'Shire': [('Axum', 2), ('Debarke', 7), ('Humera', 8)],
    'Axum': [('Shire', 2), ('Asmera', 5), ('Adwa', 1)],
    'Asmera': [('Axum', 5), ('Adigrat', 9)],
    'Adigrat': [('Adwa', 4), ('Mekelle', 4), ('Asmera', 9)],
    'Metema': [('Kartum', 19), ('Gondar', 7), ('Azezo', 1)],
    'Debarke': [('Gondar', 4), ('Shire', 7)],
    'Adwa': [('Axum', 1), ('Adigrat', 4), ('Mekelle', 7)],
    'Mekelle': [('Adwa', 7), ('Adigrat', 4), ('Sekota', 9), ('Alamata', 5)],
    'Gondar': [('Debarke', 4), ('Metema', 7), ('Azezo', 1), ],
    'Bahir Dar': [('Azezo', 7), ('Debre Tabor', 4), ('Metekel', 11), ('Injibara', 4), ('Finote Selam', 6)],
    'Azezo': [('Gondar', 1), ('Metema', 7), ('Bahir Dar', 7)],
    'Debre Tabor': [('Bahir Dar', 4), ('Lalibela', 8)],
    'Lalibela': [('Debre Tabor', 8), ('Sekota', 6), ('Woldia', 7)],
    'Sekota': [('Mekelle', 9), ('Alamata', 6), ('Lalibela', 6)],
    'Alamata': [('Sekota', 6), ('Mekele', 5), ('Samara', 11), ('Woldia', 3)],
    'Woldia': [('Dessie', 6), ('Alamata', 3), ('Lalibela', 7), ('Samara', 8)],
    'Kilbet Rasu': [('Fanti Rasu', 6)],
    'Fanti Rasu': [('Samara', 7), ('Kilbet Rasu', 6)],
    'Samara': [('Fanti Rasu', 7), ('Alamata', 11), ('Woldia', 8), ('Gabi Rasu', 9)],
    'Dessie': [('Woldia', 6), ('Kemise', 4)],
    'Kemise': [('Debre Sina', 6), ('Dessie', 4)],
    'Debre Sina': [('Kemise', 6), ('Debre Birhan', 2), ('Debre Markos', 17)],
    'Metekel': [('Bahir Dar', 11)],
    'Injibara': [('Bahir Dar', 4), ('Finote Selam', 2)],
    'Finote Selam': [('Bahir Dar', 6), ('Injibara', 2), ('Debre Markos', 3)],
    'Debre Markos': [('Finote Selam', 3), ('Debre Sina', 17)],
    'Gabi Rasu': [('Samara', 9), ('Awash', 0)],
    'Awash': [('Matahara', 1), ('Chiro', 4), ('Gabi Rasu', 5)],
    'Chiro': [('Awash', 4), ('Dire Dawa', 8)],
    'Dire Dawa': [('Chiro', 8), ('Harar', 4)],
    'Harar': [('Dire Dawa', 4), ('Babile', 2)],
    'Babile': [('Harar', 2), ('Jigjiga', 3), ('Goba', 28)],
    'Jigjiga': [('Babile', 3), ('Dega Habur', 5)],
    'Dega Habur': [('Jigjiga', 5), ('Kebri Dehar', 6)],
    'Assosa': [('Dembi Dollo', 12)],
    'Dembi Dollo': [('Assosa', 12), ('Gimbi', 6), ('Gambella', 4)],
    'Gimbi': [('Dembi Dollo', 6), ('Nekemte', 4)],
    'Nekemte': [('Gimbi', 4), ('Ambo', 9), ('Bedelle', 0)],
    'Ambo': [('Nekemte', 0), ('Addis Ababa', 0), ('Wolkite', 0)],
    'Gambella': [('Dembi Dollo', 4), ('Gore', 5)],
    'Gore': [('Gambella', 5), ('Bedelle', 6), ('Tepi', 9)],
    'Tepi': [('Gore', 9), ('Mezan Teferi', 4), ('Bonga', 8)],
    'Bonga': [('Tepi', 8), ('Mezan Teferi', 4), ('Jimma', 4), ('Dawro', 10)],
    'Mezan Teferi': [('Tepi', 4), ('Bonga', 4)],
    'Jimma': [('Bonga', 4), ('Bedelle', 7), ('Wolkite', 8)],
    'Bedelle': [('Jimma', 7), ('Gore', 6), ('Nekemte', 0)],
    'Wolkite': [('Ambo', 6), ('Jimma', 8), ('Worabe', 5)],
    'Buta Jirra': [('Worabe', 2), ('Batu', 2)],
    'Batu': [('Buta Jirra', 2), ('Adama', 4), ('Shashemene', 3)],
    'Adama': [('Batu', 4), ('Matahara', 3), ('Asella', 4), ('Addis Ababa', 3)],
    'Matahara': [('Awash', 1), ('Adama', 3)],
    'Addis Ababa': [('Ambo', 5), ('Adama', 3), ('Debre Birhan', 5)],
    'Debre Birhan': [('Addis Ababa', 5), ('Debre Sina', 2)],
    'Dawro': [('Wolaita Sodo', 6), ('Bonga', 10)],
    'Wolaita Sodo': [('Dawro', 6), ('Hossana', 4), ('Arba Minch', 0)],
    'Hossana': [('Wolaita Sodo', 4), ('Worabe', 2), ('Shashemene', 7)],
    'Worabe': [('Wolkite', 5), ('Buta Jirra', 2), ('Hossana', 2)],
    'Shashemene': [('Batu', 3), ('Hossana', 7), ('Hawassa', 1), ('Dodolla', 3)],
    'Assasa': [('Asella', 4), ('Dodolla', 1)],
    'Dodolla': [('Bale', 13), ('Assasa', 1), ('Shashemene', 3)],
    'Bale': [('Goba', 18), ('Dodolla', 13), ('Sof Oumer', 23), ('Liben', 11)],
    'Goba': [('Babile', 28), ('Sof Oumer', 6), ('Bale', 18)],
    'Sof Oumer': [('Goba', 6), ('Bale', 23), ('Gode', 23)],
    'Kebri Dehar': [('Weder', 6), ('Gode', 5), ('Dega Habur', 6)],
    'Weder': [('Kebri Dehar', 6)],
    'Gode': [('Dollo', 17), ('Kebri Dehar', 5), ('Mokadisho', 22), ('Sof Oumer', 23)],
    'Bench Maji': [('Juba', 22), ('Basketo', 5)],
    'Basketo': [('Benchi Maji', 5), ('Arba Minch', 10)],
    'Arba Minch': [('Wolaita Sodo', 0), ('Konso', 4), ('Basketo', 10)],
    'Konso': [('Arba Minch', 4), ('Yabello', 3)],
    'Hawassa': [('Shashemene', 1), ('Dilla', 3)],
    'Dilla': [('Hawassa', 3), ('Bule Hora', 4)],
    'Bule Hora': [('Dilla', 4), ('Yabello', 3)],
    'Yabello': [('Bule Hora', 3), ('Moyale', 6), ('Konso', 3)],
    'Moyale': [('Yabello', 6), ('Nairobi', 22)],
    'Liben': [('Bale', 11)],
    'Dollo': [('Gode', 17)],
    'Asella': [('Assasa', 4), ('Dodolla', 1)],
    'Werder': [('Kebri Dehar', 6)],
    'Juba': [('Bench Maji', 22)],
    'Mokadisho': [('Gode', 22)],
    'Nairobi': [('Moyale', 22)],
}

goals = ["Axum", "Gondar", "Lalibela", "Babile", "Jimma", "Bale", "Sof Oumer", "Arba Minch"]

travel = TravelEthiopia(cities, roads, start="Addis Ababa", goals=goals)
path, cost = travel.search()
print(f"Final Path: {path}, Total Cost: {cost}")
