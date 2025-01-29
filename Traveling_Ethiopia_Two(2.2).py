import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import heapq

def uniform_cost_search(start, goal, roads):
    # Priority queue to store paths with their costs
    priority_queue = []
    heapq.heappush(priority_queue, (0, start, [start]))  # (cost, current_city, path_taken)

    visited = set()  # To keep track of visited nodes

    while priority_queue:
        # Pop the city with the lowest cost
        current_cost, current_city, path = heapq.heappop(priority_queue)

        # If the current city is the goal, return the cost and path
        if current_city == goal:
            return current_cost, path

        # Skip this city if it has already been visited
        if current_city in visited:
            continue

        # Mark the current city as visited
        visited.add(current_city)

        # Explore neighbors
        for neighbor, cost in roads.get(current_city, []):
            if neighbor not in visited:
                heapq.heappush(priority_queue, (current_cost + cost, neighbor, path + [neighbor]))

    # Return None if there is no path
    return None


class TravelEthiopia:
    def __init__(self, cities, roads, start=None, goal=None, strategy=None):
        self.cities = cities
        self.roads = roads
        self.start = start
        self.goal = goal
        self.strategy = strategy
        self.order = []  # Stores the order of visited nodes for visualization

        # Build the graph for visualization
        self.G = nx.Graph()
        for city in roads:
            for neighbor, _ in roads[city]:
                self.G.add_edge(city, neighbor)

        # if start is not None and goal is not None and strategy is not None:
        #     result = self.search()
        #     print("Search Result:", result)

    def dfs(self, start, goal):
        visited = set()
        stack = [(start, [start])]  # Stack stores tuples of (current city, path)

        while stack:
            city, path = stack.pop()
            if city not in visited:
                visited.add(city)
                self.order.append(city)  # Add to visit order for visualization

                # Goal check
                if city == goal:
                    return path

                # Add neighbors in reverse order to the stack
                stack.extend(
                    reversed([(neighbor, path + [neighbor]) for neighbor, _ in self.roads.get(city, [])])
                )

        return None  # Return None if goal is not found

    def bfs(self, start, goal):
        visited = set()
        queue = deque([(start, [start])])  # Queue stores tuples of (current city, path)

        while queue:
            city, path = queue.popleft()
            if city not in visited:
                visited.add(city)
                self.order.append(city)  # Add to visit order for visualization

                # Goal check
                if city == goal:
                    return path

                # Add neighbors to the queue
                queue.extend(
                    [(neighbor, path + [neighbor]) for neighbor, _ in self.roads.get(city, [])]
                )

        return None  # Return None if goal is not found

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

    def search(self):
        # Reset visit order for each search
        self.order = []

        # Call the appropriate search method based on the strategy
        if self.strategy == "dfs":
            title = "Depth-First Search"
            result = self.dfs(self.start, self.goal)
        elif self.strategy == "bfs":
            title = "Breadth-First Search"
            result = self.bfs(self.start, self.goal)
        elif self.strategy == "ucs":
            title = "Uniform Cost Search"
            result, cost = self.ucs(self.start, self.goal)
            print(f"Path: {result}, Total Cost: {cost}")
        else:
            raise ValueError("Invalid strategy. Use 'dfs' or 'bfs'.")
        print(result)

        # Visualize the search process
        pos = nx.spring_layout(self.G,  seed=42)
        self.visualize_search(pos, title)


        return result

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
                node_color=['r' if (n == node) else 'g' if n == self.goal else 'b' for n in self.G.nodes],
                node_size=100,
                font_size=10
            )
            plt.draw()
            plt.pause(0.15)  # Pause to show each step for 1 second

            # Stop visualization if the goal is reached
            # print(node, self.goal)
            if node == self.goal:
                break
        plt.show()



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

ethiopia = TravelEthiopia(cities, roads, 'Addis Ababa', 'Nairobi', 'ucs')
ethiopia.search()
