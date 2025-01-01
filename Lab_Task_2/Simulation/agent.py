from heapq import heappush, heappop
import pygame

class Agent(pygame.sprite.Sprite):
    def __init__(self, environment, grid_size):
        super().__init__()
        self.image = pygame.Surface((grid_size, grid_size))
        self.image.fill((0, 0, 255))  # Agent color is blue
        self.rect = self.image.get_rect()
        self.grid_size = grid_size
        self.environment = environment

        self.position_Astar = [0, 0]  # Starting at the top-left corner of the grid
        self.rect.topleft = (0, 0)

        self.position_UCS = [0, 0]  # Starting at the top-left corner of the grid


        self.task_completed_Astar = 0
        self.task_completed_UCS = 0

        self.completed_tasks_Astar = []
        self.completed_tasks_UCS = []

        self.path_Astar = []  # List of positions to follow
        self.moving_Astar = False  # Flag to indicate if the agent is moving

        self.path_UCS = []  # List of positions to follow
        self.moving_UCS = False  # Flag to indicate if the agent is moving

        self.total_cost_Astar = 0  # Cost accumulator for all moves
        self.total_cost_UCS = 0

        self.last_cost_UCS = 0
        self.last_cost_Astar = 0

    def move_Astar(self):
        """Move the agent along the path."""
        if self.path_Astar:
            next_position = self.path_Astar.pop(0)
            self.position_Astar = list(next_position)
            self.rect.topleft = (self.position_Astar[0] * self.grid_size, self.position_Astar[1] * self.grid_size)
            self.total_cost_Astar += 1  # Increment cost for each move
            self.check_task_completion_Astar()
            return 1
        else:
            self.moving_Astar = False  # Stop moving when path is exhausted
        return 0

    def move_UCS(self):
        """Move the agent along the path."""
        if self.path_UCS:
            next_position = self.path_UCS.pop(0)
            self.position_UCS = list(next_position)
            self.rect.topleft = (self.position_UCS[0] * self.grid_size, self.position_UCS[1] * self.grid_size)
            self.total_cost_UCS += 1  # Increment cost for each move
            self.check_task_completion_UCS()
            return 1
        else:
            self.moving_UCS = False  # Stop moving when path is exhausted
        return 0

    def check_task_completion_Astar(self):
        """Check if the agent has reached a task location."""
        position_tuple = tuple(self.position_Astar)
        
        if position_tuple in self.environment.task_locations_Astar:
            task_number = self.environment.task_locations_Astar.pop(position_tuple)
            self.task_completed_Astar += 1
            self.completed_tasks_Astar.append(f"{task_number} (Cost {self.total_cost_Astar - self.last_cost_Astar})")
            self.last_cost_Astar = self.total_cost_Astar

    def check_task_completion_UCS(self):
        """Check if the agent has reached a task location."""
        position_tuple = tuple(self.position_UCS)
        
        if position_tuple in self.environment.task_locations_UCS:
            task_number = self.environment.task_locations_UCS.pop(position_tuple)
            self.task_completed_UCS += 1
            self.completed_tasks_UCS.append(f"{task_number} (Cost {self.total_cost_UCS - self.last_cost_UCS})")
            self.last_cost_UCS = self.total_cost_UCS

    def find_nearest_task_Astar(self):
        """Find the nearest task using A* search."""
        if not self.environment.task_locations_Astar:
            self.path_Astar = []
            self.moving_Astar = False
            return

        shortest_path = None
        for task_position in self.environment.task_locations_Astar.keys():
            path = self.find_path_to_Astar(task_position)
            if path:
                if not shortest_path or len(path) < len(shortest_path):
                    shortest_path = path
        if shortest_path:
            self.path_Astar = shortest_path[1:]  # Exclude the current position
            self.moving_Astar = True
        else:
            self.moving_Astar = []

    def find_nearest_task_UCS(self):
        """Find the nearest task using A* search."""
        if not self.environment.task_locations_UCS:
            self.path_UCS = []
            self.moving_UCS= False
            return

        shortest_path = None
        for task_position in self.environment.task_locations_UCS.keys():
            path = self.find_path_to_UCS(task_position)
            if path:
                if not shortest_path or len(path) < len(shortest_path):
                    shortest_path = path
        if shortest_path:
            self.path_UCS = shortest_path[1:]  # Exclude the current position
            self.moving_UCS = True
        else:
            self.moving_UCS = []

    def find_path_to_Astar(self, target):
        """Find a path to the target position using A* search."""
        start = tuple(self.position_Astar)
        goal = target
        open_set = []
        heappush(open_set, (0, start))  # Priority queue with (cost, position)
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        while open_set:
            _, current = heappop(open_set)

            if current == goal:
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()  # Reverse the path to get the order from start to goal
                return path

            for neighbor in self.get_neighbors(*current):
                tentative_g_score = g_score[current] + 1  # Each move has a cost of 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    heappush(open_set, (f_score[neighbor], neighbor))

        return None  # No path found

    def find_path_to_UCS(self, target):
        """Find a path to the target position using UCS."""
        start = tuple(self.position_UCS)
        goal = target
        queue = [(0, start, [start])]
        visited = set()

        while queue:
            cost, vertex, path = heappop(queue)
            if vertex in visited:
                continue
            visited.add(vertex)
            if vertex == goal:
                return path
            for neighbor in self.get_neighbors(*vertex):
                heappush(queue, (cost + 1, neighbor, path + [neighbor]))
        return None


    def heuristic(self, position, goal):
        """Calculate Manhattan distance as the heuristic."""
        return abs(position[0] - goal[0]) + abs(position[1] - goal[1])

    def get_neighbors(self, x, y):
        """Get walkable neighboring positions."""
        neighbors = []
        directions = [("up", (0, -1)), ("down", (0, 1)), ("left", (-1, 0)), ("right", (1, 0))]
        for _, (dx, dy) in directions:
            nx, ny = x + dx, y + dy
            if self.environment.is_within_bounds(nx, ny) and not self.environment.is_barrier(nx, ny):
                neighbors.append((nx, ny))
        return neighbors
    
    


