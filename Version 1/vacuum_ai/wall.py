from vacuum_ai.robot import Robot
from vacuum_ai.agent import Agent

class Wall:

    def __init__(self, position):
        self.position = position

    def __str__(self):
        return '|🚧|'
