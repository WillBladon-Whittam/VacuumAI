from typing import Any

from vacuum_ai.robot import Robot
from vacuum_ai.agent import Agent

class BaseStation(Agent):
    """
    The Base Station / Charger Intelligent Agent
    """

    def __init__(self, position, direction):
        super().__init__(position)
        self.direction = direction
        
    def sense(self, environment) -> list[dict[tuple[int, int], Any]]:
        """
        Override the sense function from the Agent abstract class.
        This is needed as the sense is based on the direction the robot is facing.

        Args:
            environment (Enviroment): The enviroment of the room

        Returns:
            list[dict[tuple[int, int], Any]]: A dictionary where each item is a dictionaty, 
            where the key is the grid location, and the value is the object (what is there) 
        """
        direction_map = {
            "u": (0, -1), 
            "d": (0, 1),
            "l": (-1, 0),
            "r": (1, 0)
        }
        
        return environment.get_cells([tuple(sum(x) for x in zip(self.position, direction_map[self.direction]))])

    def decide(self, percept: dict[tuple[int, int], Any]) -> Robot:
        """
        Decide whether to recharge the Robot

        Args:
            percept (dict[tuple[int, int], Any]): The location and what is there

        Returns:
            Robot: Returns the robot to recharge
            None: No robot infront so don't recharge
        """
        for _, item in percept.items():
            if isinstance(item, Robot):
                return item

    def act(self, environment) -> None:
        """
        First sense the enviroment around the base station.
        Make a decision based on whether to recharge the robot if its in position.
        """
        cell = self.sense(environment)
        robot = self.decide(cell)

        if robot is not None:
            robot.battery_life = 100

    def __str__(self):
        if self.direction == "u":
            return '↑🔋↑'
        elif self.direction == "d":
            return '↓🔋↓'
        elif self.direction == "l":
            return '←🔋←'
        elif self.direction == "r":
            return '→🔋→'
