from vacuum_ai.robot import Robot
from vacuum_ai.agent import Agent

class BaseStation(Agent):

    def __init__(self, position, direction):
        super().__init__(position)
        self.direction = direction

    def decide(self, percept):
        for _, item in percept.items():
            if isinstance(item, Robot):
                return item

    def act(self, environment):
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
