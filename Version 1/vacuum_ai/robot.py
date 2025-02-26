from typing import Literal, Any

from vacuum_ai.agent import Agent
import random
import heapq


class Robot(Agent):
    """
    The Robot Vacuum Intelligent Agent
    """

    def __init__(self, position: tuple[int, int], direction: Literal["^", "v", "<", ">"]):
        super().__init__(position)
        self.direction = direction

        self.battery_life = 100

    def decide(self, percept: dict[tuple[int, int], Any]) -> tuple[str, str | int]:
        """
        Decide on what the vacuums next move is.
        Logic:
            - Pick at random to move or rotate
            - If move, move in the direction the robot is facing
            - if rotate, or if the robot is facing an invalid move location, then choose a random rotation,
              its current orientation is not included, so the robot doesn't waste a turn

        Args:
            percept (dict[tuple[int, int], Any]): The location and what is there

        Returns:
            tuple[str, str | int]: The first item in the tuple reutrned is the action, 
            the next item is either the location to move to, or the orentation to change to
        """
        # Get all the valid positions around the robot
        valid_cells = [location for location, item in percept.items() if item == " "]

        # Pick a random action
        selected_option = random.choice(["rotate", "move"])
        
        # Map the direction to each position around the robot
        current_position_direction = {
                "^": (self.position[0], self.position[1] - 1),
                "v": (self.position[0], self.position[1] + 1),
                "<": (self.position[0] - 1, self.position[1]),
                ">": (self.position[0] + 1, self.position[1])
            }
        reverse_dict = {v: k for k, v in current_position_direction.items()}

        if selected_option == "move":
            # If move is randomly selected, move in the direction the robot is facing
            target_move = current_position_direction[self.direction]

            # Only move if the way the robot is going to is valid, otherwise continue to choose a orientation
            if target_move in valid_cells:
                return "move", target_move
  
        # Update the valid cells to remove the cells current direction - as we don't want a cycle used without the robot changing anything      
        valid_cells = [move for move in valid_cells if reverse_dict[move[0], move[1]] != self.direction]
        
        # This covers the edge case where the robot is surrounded by 3 invalid location, and is facing the only valid way,
        # and the robot randomly chose to change its orientation. This isn't possible, so the robots only option is to move forward.
        if valid_cells:
            # Select a random cell from the valid ones
            selected_move = random.choice(valid_cells)

            # Rotate the robot based on its randomly chosen orientation
            move_direction = (selected_move[0] , selected_move[1])
            return "rotate", reverse_dict[move_direction]
        
        target_move = current_position_direction[self.direction]
        return "move", target_move
    
    def act(self, environment):
        """
        First sense the enviroment around the robot.
        Make a decision, and act on that decision.
        """
        cell = self.sense(environment)
        action, result = self.decide(cell)

        if action == "move":
            environment.move_robot(self, result)
        elif action == "rotate":
            self.direction = result
            
        self.battery_life -= 1

    def __str__(self):
        if self.direction == "^":
            return '↑🤖↑'
        elif self.direction == "v":
            return '↓🤖↓'
        elif self.direction == "<":
            return '←🤖←'
        elif self.direction == ">":
            return '→🤖→'

