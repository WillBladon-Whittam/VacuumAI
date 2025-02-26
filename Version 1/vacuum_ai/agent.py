from abc import ABC, abstractmethod
from typing import Any


class Agent(ABC):
    """
    Abstract class that is inheritented by all Intelligent Agents.
    """

    def __init__(self, position: tuple[int, int]):
        self.position = position
        self.direction_offsets = {
            "up": (-1, 0),
            "right": (0, 1),
            "down": (1, 0),
            "left": (0, -1)
        }

    def sense(self, environment, directions = ["up", "right", "down", "left"]) -> list[dict[tuple[int, int], Any]]:
        """
        Sense function which looks at grid positions around it.

        Args:
            environment (Enviroment): The enviroment of the room
            directions (list): Which directions the agent should sense. Defaults to ["up", "right", "down", "left"].

        Returns:
            list[dict[tuple[int, int], Any]]: A dictionary where each item is a dictionaty, 
            where the key is the grid location, and the value is the object (what is there) 
        """
        neighbours = []
        for direction in directions:
            row_offset, col_offset = self.direction_offsets[direction]
            neighbours.append((self.position[0] + row_offset, self.position[1] + col_offset))

        return environment.get_cells(neighbours)

    @abstractmethod
    def decide(self, percept: dict[tuple[int,int], Any]):
        pass

    @abstractmethod
    def act(self, environment):
        pass
