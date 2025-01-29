class MiniMaxSearch:
    def __init__(self, roads):
        self.roads = roads
        self.best_path = []

    def is_adversary_edge(self, current_node, neighbor):
        """Returns True if the path between current_node and the neighbor has an adversary."""
        # Find if any of the neighbors' path is adversarial (has adversary = True)
        for neighbor_city, is_blocked in self.roads[current_node]['neighbors']:
            if neighbor_city == neighbor and is_blocked:
                return True
        return False

    def minimax(self, current_node, is_maximizing_player, visited):
        # If the current node has an adversary, return an invalid utility.
        # Do not explore adversary paths
        for neighbor, is_blocked in self.roads[current_node]['neighbors']:
            if self.is_adversary_edge(current_node, neighbor):
                return float('-inf'), []  # Blocked due to adversary

        # Base case: if the current node is terminal, return its utility.
        if self.roads[current_node]['terminal']:
            return self.roads[current_node]['utility'], [current_node]

        # Initialize the best value to be maximized or minimized.
        best_value = float('-inf') if is_maximizing_player else float('inf')
        best_path = []

        # Add the current node to the visited set to avoid revisiting it
        visited.add(current_node)

        # Explore all neighbors of the current node
        for neighbor, is_blocked in self.roads[current_node]['neighbors']:
            # Skip if the neighbor is blocked, already visited, or has an adversary
            if is_blocked or neighbor in visited:
                continue

            # Recursive call to the minimax function
            value, path = self.minimax(neighbor, not is_maximizing_player, visited)

            if is_maximizing_player and value > best_value:
                best_value = value
                best_path = [current_node] + path
            elif not is_maximizing_player and value < best_value:
                best_value = value
                best_path = [current_node] + path

        # Remove the current node from the visited set when backtracking
        visited.remove(current_node)

        return best_value, best_path

    def get_best_path(self, start_node):
        # Start the minimax search from the start node with an empty visited set
        visited = set()

        value, path = self.minimax(start_node, is_maximizing_player=True, visited=visited)
        self.best_path = path
        return path, value

roads = {
    'Shambu': { 'utility': 4, 'neighbors': [('Gedo', False)], 'terminal': True },
    'Fincha': { 'utility': 5, 'neighbors': [('Gedo', False)], 'terminal': True },
    'Gimbi': { 'utility': 8, 'neighbors': [('Nekemte', False)], 'terminal': True },
    'Gedo': { 'utility': 0, 'neighbors': [('Shambu', False), ('Fincha', False)], 'terminal': False },
    'Nekemte': { 'utility': 0, 'neighbors': [('Gimbi', False), ('Limu', False)], 'terminal': False },
    'Hossana': { 'utility': 6, 'neighbors': [('Worabe', False)], 'terminal': True },
    'Durame': { 'utility': 5, 'neighbors': [('Worabe', False)], 'terminal': True },
    'Bench Naji': { 'utility': 5, 'neighbors': [('Wolkite', False)], 'terminal': True },
    'Tepi': { 'utility': 6, 'neighbors': [('Wolkite', False)], 'terminal': True },
    'Wolkite': { 'utility': 0, 'neighbors': [('Tepi', False), ('Bench Naji', False)], 'terminal': False },
    'Buta Jirra': { 'utility': 0, 'neighbors': [('Addis Ababa', False), ('Wolkite', False), ('Worabe', False)], 'terminal': False },
    'Adama': { 'utility': 0, 'neighbors': [('Addis Ababa', True), ('Diredawa', False), ('Mojo', False)], 'terminal': False },
    'Diredawa': { 'utility': 0, 'neighbors': [('Chiro', False), ('Harar', False)], 'terminal': False },
    'Harar': { 'utility': 10, 'neighbors': [('Diredawa', False)], 'terminal': True },
    'Chiro': { 'utility': 6, 'neighbors': [('Diredawa', False)], 'terminal': True },
    'Dilla': { 'utility': 9, 'neighbors': [('Mojo', False)], 'terminal': True },
    'Kaffa': { 'utility': 7, 'neighbors': [('Mojo', False)], 'terminal': True },
    'Addis Ababa': { 'utility': 0, 'neighbors': [('Adama', False), ('Ambo', False), ('Buta Jirra', False)], 'terminal': False },
    'Mojo': { 'utility': 0, 'neighbors': [('Adama', True), ('Dilla', False), ('Kaffa', False)], 'terminal': False },
    'Worabe': { 'utility': 0, 'neighbors': [('Hossana', False), ('Durame', False), ('Buta Jirra', False)], 'terminal': False },
    'Limu': { 'utility': 0, 'neighbors': [('Nekemte', False)], 'terminal': True },
    'Ambo': { 'utility': 0, 'neighbors': [('Addis Ababa', False), ('Nekemte', False), ('Gedo', False)], 'terminal': True }
}


# Create an instance of the MiniMaxSearch class
search_agent = MiniMaxSearch(roads)

# Get the best path starting from a valid city
best_path, best_value = search_agent.get_best_path('Addis Ababa')  # Start from a non-adversary city

print("Best path:", best_path)
print("Best value (utility):", best_value)
