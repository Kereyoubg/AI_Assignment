from random import random
import time
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

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
                node_color=['r' if n == node else 'b' for n in self.G.nodes],
                node_size=100,
                font_size=10
            )
            plt.draw()
            plt.pause(2)  # Pause to show each step for 1 second

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
    'Humera': [('Shire', 0), ('Gondar', 0)],
    'Shire': [('Axum', 0), ('Debarke', 0)],
    'Kartum': [('Humera', 0), ('Metema', 0)],
    'Axum': [('Asmera', 0), ('Adwa', 0)],
    'Asmera': [('Axum', 0), ('Adigrat', 0)],
    'Adigrat': [('Adwa', 0), ('Mekelle', 0), ('Asmera', 0)],
    'Metema': [('Kartum', 0), ('Gondar', 0), ('Azezo', 0)],
    'Debarke': [('Gondar', 0), ('Shire', 0)],
    'Adwa': [('Axum', 0), ('Adigrat', 0), ('Mekelle', 0)],
    'Mekelle': [('Adwa', 0), ('Adigrat', 0), ('Sekota', 0), ('Alamata', 0)],
    'Gondar': [('Debarke', 0), ('Metema', 0), ('Azezo', 0)],
    'Bahir Dar': [('Azezo', 0), ('Debre Tabor', 0), ('Metekel', 0), ('Injibara', 0), ('Finote Selam', 0)],
    'Azezo': [('Gondar', 0), ('Metema', 0), ('Bahir Dar', 0)],
    'Debre Tabor': [('Bahir Dar', 0), ('Lalibela', 0)],
    'Lalibela': [('Debre Tabor', 0), ('Sekota', 0), ('Woldia', 0)],
    'Sekota': [('Mekelle', 0), ('Alamata', 0), ('Lalibela', 0)],
    'Alamata': [('Sekota', 0), ('Mekele', 0), ('Samara', 0), ('Woldia', 0)],
    'Woldia': [('Dessie', 0), ('Alamata', 0), ('Lalibela', 0), ('Samara', 0)],
    'Kilbet Rasu': [('Fanti Rasu', 0)],
    'Fanti Rasu': [('Samara', 0), ('Kilbet Rasu', 0)],
    'Samara': [('Fanti Rasu', 0), ('Alamata', 0), ('Woldia', 0), ('Gabi Rasu', 0)],
    'Dessie': [('Woldia', 0), ('Kemise', 0)],
    'Kemise': [('Debre Sina', 0), ('Dessie', 0)],
    'Debre Sina': [('Kemise', 0), ('Debre Birhan', 0), ('Debre Markos', 0)],
    'Metekel': [('Bahir Dar', 0), ('Assosa', 0)],
    'Injibara': [('Bahir Dar', 0), ('Finote Selam', 0)],
    'Finote Selam': [('Bahir Dar', 0), ('Injibara', 0), ('Debre Markos', 0)],
    'Debre Markos': [('Finote Selam', 0), ('Debre Sina', 0)],
    'Gabi Rasu': [('Samara', 0), ('Awash', 0)],
    'Awash': [('Matahara', 0), ('Chiro', 0), ('Gabi Rasu', 0)],
    'Chiro': [('Awash', 0), ('Dire Dawa', 0)],
    'Dire Dawa': [('Chiro', 0), ('Harar', 0)],
    'Harar': [('Dire Dawa', 0), ('Babile', 0)],
    'Babile': [('Harar', 0), ('Jigjiga', 0)],
    'Jigjiga': [('Babile', 0), ('Dega Habur', 0)],
    'Dega Habur': [('Jigjiga', 0), ('Kebri Dehar', 0), ('Goba', 0)],
    'Assosa': [('Metekel', 0), ('Dembi Dollo', 0)],
    'Dembi Dollo': [('Assosa', 0), ('Gimbi', 0), ('Gambella', 0)],
    'Gimbi': [('Dembi Dollo', 0), ('Nekemte', 0)],
    'Nekemte': [('Gimbi', 0), ('Ambo', 0), ('Bedelle', 0)],
    'Ambo': [('Nekemte', 0), ('Addis Ababa', 0), ('Wolkite', 0)],
    'Gambella': [('Dembi Dollo', 0), ('Gore', 0)],
    'Gore': [('Gambella', 0), ('Bedelle', 0), ('Tepi', 0)],
    'Tepi': [('Gore', 0), ('Mezan Teferi', 0), ('Bonga', 0)],
    'Bonga': [('Tepi', 0), ('Mezan Teferi', 0), ('Jimma', 0), ('Dawro', 0)],
    'Mezan Teferi': [('Tepi', 0), ('Bonga', 0), ('Basketo', 0)],
    'Jimma': [('Bonga', 0), ('Bedelle', 0), ('Wolkite', 0)],
    'Bedelle': [('Jimma', 0), ('Gore', 0), ('Nekemte', 0)],
    'Wolkite': [('Ambo', 0), ('Jimma', 0), ('Worabe', 0)],
    'Buta Jirra': [('Worabe', 0), ('Batu', 0)],
    'Batu': [('Buta Jirra', 0), ('Adama', 0), ('Shashemene', 0)],
    'Adama': [('Batu', 0), ('Matahara', 0), ('Asella', 0), ('Addis Ababa', 0)],
    'Matahara': [('Awash', 0), ('Adama', 0)],
    'Addis Ababa': [('Ambo', 0), ('Adama', 0), ('Debre Birhan', 0)],
    'Debre Birhan': [('Addis Ababa', 0), ('Debre Sina', 0)],
    'Dawro': [('Basketo', 0), ('Wolaita Sodo', 0), ('Bonga', 0)],
    'Wolaita Sodo': [('Dawro', 0), ('Hossana', 0), ('Arba Minch', 0)],
    'Hossana': [('Wolaita Sodo', 0), ('Worabe', 0), ('Shashemene', 0)],
    'Worabe': [('Wolkite', 0), ('Buta Jirra', 0), ('Hossana', 0)],
    'Shashemene': [('Batu', 0), ('Hossana', 0), ('Hawassa', 0), ('Dodolla', 0)],
    'Assasa': [('Asella', 0), ('Dodolla', 0)],
    'Dodolla': [('Bale', 0), ('Assasa', 0), ('Shashemene', 0)],
    'Bale': [('Goba', 0), ('Dodolla', 0), ('Sof Oumer', 0), ('Liben', 0)],
    'Sof Oumer': [('Goba', 0), ('Bale', 0), ('Kebri Dehar', 0)],
    'Kebri Dehar': [('Weder', 0), ('Sof Oumer', 0), ('Gode', 0), ('Dega Habur', 0)],
    'Weder': [('Kebri Dehar', 0)],
    'Gode': [('Dollo', 0), ('Kebri Dehar', 0), ('Mokadisho', 0)],
    'Bench Maji': [('Juba', 0), ('Basketo', 0)],
    'Basketo': [('Benchi Maji', 0), ('Mezan Teferi', 0), ('Dawro', 0), ('Arba Minch', 0)],
    'Arba Minch': [('Wolaita Sodo', 0), ('Konso', 0), ('Basketo', 0)],
    'Konso': [('Arba Minch', 0), ('Yabello', 0)],
    'Hawassa': [('Shashemene', 0), ('Dilla', 0)],
    'Dilla': [('Hawassa', 0), ('Bule Hora', 0)],
    'Bule Hora': [('Dilla', 0), ('Yabello', 0)],
    'Yabello': [('Bule Hora', 0), ('Moyale', 0), ('Konso', 0)],
    'Moyale': [('Yabello', 0), ('Nairobi', 0)],
    'Liben': [('Bale', 0)],
    'Dollo': [('Bale', 0), ('Assasa', 0), ('Shashemene', 0)],
    'Asella': [('Assasa', 0), ('Adama', 0)],
    'Werder': [('Kebri Dehar', 0)],
    'Juba': [('Bench Maji', 0)],
    'Mokadisho': [('Gode', 0)],
    'Nairobi': [('Moyale', 0)],
    'Goba': [('Bale', 0), ('Dega Habur', 0), ('Sof Oumer', 0)]
}

ethiopia = TravelEthiopia(cities, roads, 'Moyale', 'Nairobi', 'bfs')
ethiopia.search()
