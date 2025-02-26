from vacuum_ai.robot import Robot
from vacuum_ai.base_station import BaseStation
from vacuum_ai.wall import Wall


class Environment:

    def __init__(self, map_path):
        self.file_path = map_path
        self.world = self.load_assets(self.load_map())

    def load_map(self):
        try:
            with open(self.file_path) as f:
                world_map = row = [[col.lower() for col in line.strip()] for line in f]

                # quick error check
                first_row = len(world_map[0])
                for row in world_map:
                    if len(row) != first_row:
                        raise Exception("Map rows are not even")
                return world_map
        except FileNotFoundError:
            print(f"File not found")
        except PermissionError:
            print(f"File read permissions were denied")
        except IOError as e:
            print(f"IO error: {e}")

        return []

    def load_assets(self, world_map:list):
        for i in range(len(world_map)):
            for j in range(len(world_map[i])):
                if world_map[i][j] in ["u", "d", "l", "r"]:
                    world_map[i][j] = BaseStation((j, i), world_map[i][j])
                elif world_map[i][j] in ["^", "v", "<", ">"]:
                    world_map[i][j] = Robot((j, i), world_map[i][j])
                elif world_map[i][j] == "x":
                    world_map[i][j] = Wall((j, i))
        return world_map
    
    def get_cells(self, positions:list) -> dict[tuple[int,int],...]:
        cells = {}
        for pos in positions:
            cells[pos] = self.world[pos[1]][pos[0]]
        return cells
    
    def get_robot_location(self):
        for i in range(len(self.world)):
            for j in range(len(self.world[i])):
                if isinstance(self.world[i][j], Robot):
                    return self.world[i][j]
                
    def move_robot(self, robot, move_to):
        current_location = robot.position
        self.world[current_location[1]][current_location[0]] = " "
        self.world[move_to[1]][move_to[0]] = robot
        robot.position = move_to

    def __str__(self):
        out = ""
        for row in self.world:
            for col in row:
                out += f"{col}\t"
            out += "\n"
        return out

