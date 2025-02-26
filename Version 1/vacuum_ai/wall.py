from vacuum_ai.robot import Robot
from vacuum_ai.agent import Agent

class Wall:
    """
    Wall object, just to print the walls out with a nice emoji
    """

    def __init__(self, position):
        self.position = position

    def __str__(self):
        return '|🚧|'
