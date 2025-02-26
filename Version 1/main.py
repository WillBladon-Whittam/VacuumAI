import time
import argparse

from vacuum_ai.robot import Robot
from vacuum_ai.base_station import BaseStation
from vacuum_ai.environment import Environment

if __name__ == "__main__":

    # Specify an interval between cycles
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interval', nargs='?', const=1, type=int, default=1)
    parser.add_argument('-n', '--num-cycles', nargs='?', const=1000, type=int, default=1000)
    args = parser.parse_args()
    
    # Initilise the enviroment and get the robot and base station
    enviroment = Environment("floorplan.txt")
    robot = enviroment.get_location(Robot)
    base_station = enviroment.get_location(BaseStation)

    # Start running the cycle
    for i in range(args.num_cycles):
        time.sleep(args.interval)
        print("Battery", robot.battery_life, "%")
        print(enviroment)
        if robot.battery_life == 0:
            quit()
        robot.act(enviroment)
        base_station.act(enviroment)