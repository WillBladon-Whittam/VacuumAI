from vacuum_ai.environment import Environment

if __name__ == "__main__":
    
    enviroment = Environment("floorplan.txt")
    robot = enviroment.get_robot_location()

    for i in range(1):
        print(enviroment)
        # robot1.act(e)
