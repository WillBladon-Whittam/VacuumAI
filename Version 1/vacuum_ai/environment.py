from typing import Any

from vacuum_ai.robot import Robot
from vacuum_ai.base_station import BaseStation
from vacuum_ai.wall import Wall


class Environment:
    """
    The Enviroment / Room to be vacuumed
    """

    def __init__(self, map_path):
        self.file_path = map_path
        self.world = self.load_assets(self.load_map())

    def load_map(self):
        """
        Load the map from the txt file to a 2D list.
        """
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

    def load_assets(self, world_map: list[list[str]]) -> list[list[Any]]:
        """
        Replace the ASCII Characters in the map with object

        Args:
            world_map (list[list[str]]): A 2D list of the envioment

        Returns:
            list[list[Any]]: A 2D list of the envioment with objects
        """
        for i in range(len(world_map)):
            for j in range(len(world_map[i])):
                if world_map[i][j] in ["u", "d", "l", "r"]:
                    world_map[i][j] = BaseStation((j, i), world_map[i][j])
                elif world_map[i][j] in ["^", "v", "<", ">"]:
                    world_map[i][j] = Robot((j, i), world_map[i][j])
                elif world_map[i][j] == "x":
                    world_map[i][j] = Wall((j, i))
        return world_map
    
    def get_cells(self, positions: list[tuple[int, int]]) -> dict[tuple[int,int], Any]:
        """
        Get the cells from the grid coordinates

        Args:
            positions (list): A list of coordinates to get from the map

        Returns:
            dict[tuple[int,int], Any]: The location and what is there
        """
        cells = {}
        for pos in positions:
            cells[pos] = self.world[pos[1]][pos[0]]
        return cells
    
    def get_location(self, obj_type) -> object:
        """
        Get the location of a specific object

        Args:
            obj_type (Any): The class to get the location for

        Returns:
            object: The found object in the map
        """
        for row in self.world:
            for cell in row:
                if isinstance(cell, obj_type):
                    return cell
                
    def move_robot(self, robot: Robot, move_to: tuple[int, int]):
        """
        Move the robot in the enviroment

        Args:
            robot (Robot): The robot to move
            move_to (tuple[int, int]): The coordinates to move the robot to
        """
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

