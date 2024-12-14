'''
--- Part Two ---

During the bathroom break, someone notices that these robots seem awfully similar to ones built and used at the North Pole. If they're the same type of robots, they should have a hard-coded Easter egg: very rarely, most of the robots should arrange themselves into a picture of a Christmas tree.

What is the fewest number of seconds that must elapse for the robots to display the Easter egg?

'''
import re
import matplotlib.pyplot as plt
import numpy as np

def main():
    robots = parse_input('data/aoc24_input_14.txt')
#    visualize_situation(robots, 7051)

    for time in range(10000):
        print(time)
        print_map(robots)
        for robot in robots:
            robot.move()

def parse_input(inputfile):
    '''parse an input file where each line represents a robot position and velocity in the format:
    p=4,11 v=-61,-65
    '''
    robots = []
    robot_pattern = re.compile(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)')
    with open(inputfile) as f:
        for line in f.readlines():
            match = robot_pattern.match(line.strip())
            pos = (int(match.group(1)), int(match.group(2)))
            vel = (int(match.group(3)), int(match.group(4)))
            robots.append(Robot(pos, vel))
    return robots

def visualize_situation(robots, time, map_width=101, map_height=103):
    '''visualize the situation of the robots at a given time
    '''
    plt.ion()
    fig, ax = plt.subplots()
    # Create matrix of positions
    matrix = np.zeros((map_height, map_width))
    for robot in robots:
        x, y = robot.move(time)
        matrix[y][x] = 1

    # Update visualization
    ax.clear()
    ax.imshow(matrix, cmap='binary')
    plt.title(f'Time: {time}')
    plt.pause(100)

def visualize_robot_positions(robots, map_width=101, map_height=103):
    plt.ion()
    fig, ax = plt.subplots()
    time = 0
    while True:
        print(time)
        print_map(robots)
        # Create matrix of positions
        matrix = np.zeros((map_height, map_width))
        for robot in robots:
            x, y = robot.position
            matrix[y][x] = 1
        
        # Update visualization
        ax.clear()
        ax.imshow(matrix, cmap='binary')
        plt.title(f'Time: {time}')
        plt.pause(0.2)
        
        # Update robot positions
        for robot in robots:
            robot.move(1)
        time += 1

def print_map(robots, map_width=101, map_height=103):
    '''print a map of the robots and their positions
    '''
    map = [['.' for _ in range(map_width)] for _ in range(map_height)]
    for robot in robots:
        map[robot.position[1]][robot.position[0]] = '#'
    for row in map:
        print(''.join(row))

def get_safety_factor(robots, time=100):
    '''get the safety factor of a list of robots after a given number of seconds
    '''
    quadrant_counts = [0,0,0,0,0] # 0 index is the middle
    for robot in robots:
        position = robot.move(time)
        quadrant = robot.get_quadrant()
        quadrant_counts[quadrant] += 1
    safety_factor = 1
    for count in quadrant_counts[1:]:
        safety_factor *= count
    return safety_factor

class Robot():

    def __init__(self, pos=(0,0), vel=(0,0), map_width=101, map_height=103):
        self.position = pos
        self.velocity = vel
        self.map_dimensions = (map_width, map_height)

    def move(self, time=1):
        for _ in range(time):
            self.position = ((self.position[0] + self.velocity[0])%self.map_dimensions[0], (self.position[1] + self.velocity[1])%self.map_dimensions[1])
        return self.position

    def get_quadrant(self):
        '''get the quadrant of a robot's position
        '''
        if self.position[0] == (self.map_dimensions[0]-1)/2 or self.position[1] == (self.map_dimensions[1]-1)/2:
            return 0 # middle
        elif self.position[0] > (self.map_dimensions[0]-1)/2: # right half
            if self.position[1] > (self.map_dimensions[1]-1)/2: # bottom half
                return 1 # bottom right
            else:
                return 4 # top right
        elif self.position[0] < (self.map_dimensions[0]-1)/2: # left half
            if self.position[1] > (self.map_dimensions[1]-1)/2: # bottom half
                return 2 # bottom left
            else:
                return 3 # top left
        else:
            return 0 # should not happen
    
    def __str__(self):
        return f"Robot at {self.position} with velocity {self.velocity} in quadrant {self.get_quadrant()}"
if __name__ == '__main__':
    main()
