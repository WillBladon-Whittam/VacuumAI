from vacuum_ai.agent import Agent
import random
import heapq


class Robot(Agent):

    def __init__(self, position: tuple[int, int], direction):
        super().__init__(position)
        self.direction = direction

        self.battery_life = 5


    def decide(self, percept: dict[tuple[int, int], ...]):
        ...

    def act(self, environment):
        cell = self.sense(environment)
        action, location = self.decide(cell)

        if action == "move":
            self.move(environment, location)
        elif action == "random_move":
            self.move(environment, random.choice(location))
        elif action == "put_out_flame":
            self.flames.remove(location)
            self.world[location[1]][location[0]] = " "
            environment.put_out_flame(location)
            self.water_level -= 5

    def move(self, environment, to):
        environment.move_robot(self, to)

    def __str__(self):
        if self.direction == "^":
            return '↑🤖↑'
        elif self.direction == "v":
            return '↓🤖↓'
        elif self.direction == "<":
            return '←🤖←'
        elif self.direction == ">":
            return '→🤖→'

    # MANHATTAN DISTANCE FUNCTIONS
    def calc_path(self, start, goal, viable):
        p_queue = []
        heapq.heappush(p_queue, (0, start))

        directions = {
            "right": (0, 1),
            "left": (0, -1),
            "up": (-1, 0),
            "down": (1, 0)
        }
        predecessors = {start: None}
        g_values = {start: 0}

        while len(p_queue) != 0:
            current_cell = heapq.heappop(p_queue)[1]
            if current_cell == goal:
                return self.get_path(predecessors, start, goal)
            for direction in ["up", "right", "down", "left"]:
                row_offset, col_offset = directions[direction]
                neighbour = (current_cell[0] + row_offset, current_cell[1] + col_offset)

                if self.viable_move(neighbour[0], neighbour[1], viable) and neighbour not in g_values:
                    cost = g_values[current_cell] + 1
                    g_values[neighbour] = cost
                    f_value = cost + self.calc_distance(goal, neighbour)
                    heapq.heappush(p_queue, (f_value, neighbour))
                    predecessors[neighbour] = current_cell

    def get_path(self, predecessors, start, goal):
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = predecessors[current]
        path.append(start)
        path.reverse()
        return path

    def viable_move(self, x, y, viable):
        if 0 <= x < len(self.world) and 0 <= y < len(self.world[0]):
            for viable_move in viable:
                if self.world[y][x] == viable_move:
                    return True
        return False

    def calc_distance(self, point1: tuple[int, int], point2: tuple[int, int]):
        x1, y1 = point1
        x2, y2 = point2
        return abs(x1 - x2) + abs(y1 - y2)

    # END OF MANHATTAN DISTANCE FUNCTIONS
