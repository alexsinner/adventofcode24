'''
--- Part Two ---

The lanternfish use your information to find a safe moment to swim in and turn off the malfunctioning robot! Just as they start preparing a festival in your honor, reports start coming in that a second warehouse's robot is also malfunctioning.

This warehouse's layout is surprisingly similar to the one you just helped. There is one key difference: everything except the robot is twice as wide! The robot's list of movements doesn't change.

To get the wider warehouse's map, start with your original map and, for each tile, make the following changes:

    If the tile is #, the new map contains ## instead.
    If the tile is O, the new map contains [] instead.
    If the tile is ., the new map contains .. instead.
    If the tile is @, the new map contains @. instead.

This will produce a new warehouse map which is twice as wide and with wide boxes that are represented by []. (The robot does not change size.)

The larger example from before would now look like this:

####################
##....[]....[]..[]##
##............[]..##
##..[][]....[]..[]##
##....[]@.....[]..##
##[]##....[]......##
##[]....[]....[]..##
##..[][]..[]..[][]##
##........[]......##
####################

Because boxes are now twice as wide but the robot is still the same size and speed, boxes can be aligned such that they directly push two other boxes at once. For example, consider this situation:

#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^

After appropriately resizing this map, the robot would push around these boxes as follows:

Initial state:
##############
##......##..##
##..........##
##....[][]@.##
##....[]....##
##..........##
##############

Move <:
##############
##......##..##
##..........##
##...[][]@..##
##....[]....##
##..........##
##############

Move v:
##############
##......##..##
##..........##
##...[][]...##
##....[].@..##
##..........##
##############

Move v:
##############
##......##..##
##..........##
##...[][]...##
##....[]....##
##.......@..##
##############

Move <:
##############
##......##..##
##..........##
##...[][]...##
##....[]....##
##......@...##
##############

Move <:
##############
##......##..##
##..........##
##...[][]...##
##....[]....##
##.....@....##
##############

Move ^:
##############
##......##..##
##...[][]...##
##....[]....##
##.....@....##
##..........##
##############

Move ^:
##############
##......##..##
##...[][]...##
##....[]....##
##.....@....##
##..........##
##############

Move <:
##############
##......##..##
##...[][]...##
##....[]....##
##....@.....##
##..........##
##############

Move <:
##############
##......##..##
##...[][]...##
##....[]....##
##...@......##
##..........##
##############

Move ^:
##############
##......##..##
##...[][]...##
##...@[]....##
##..........##
##..........##
##############

Move ^:
##############
##...[].##..##
##...@.[]...##
##....[]....##
##..........##
##..........##
##############

This warehouse also uses GPS to locate the boxes. For these larger boxes, distances are measured from the edge of the map to the closest edge of the box in question. So, the box shown below has a distance of 1 from the top edge of the map and 5 from the left edge of the map, resulting in a GPS coordinate of 100 * 1 + 5 = 105.

##########
##...[]...
##........

In the scaled-up version of the larger example from above, after the robot has finished all of its moves, the warehouse would look like this:

####################
##[].......[].[][]##
##[]...........[].##
##[]........[][][]##
##[]......[]....[]##
##..##......[]....##
##..[]............##
##..@......[].[][]##
##......[][]..[]..##
####################

The sum of these boxes' GPS coordinates is 9021.

Predict the motion of the robot and boxes in this new, scaled-up warehouse. What is the sum of all boxes' final GPS coordinates?
'''
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from matrix import Matrix

def main():
    warehouse_map = WarehouseMap.from_inputfile('data/aoc24_input_15.txt')
#    warehouse_map = WarehouseMap.from_inputfile('data/test15.txt')
    # warehouse_map.visualize()
    for instruction in warehouse_map.instructions:
        warehouse_map.move(instruction)
    print(warehouse_map.get_box_gps())
#    warehouse_map.visualize()
#    warehouse_map.run_with_animation()

class WarehouseMap(Matrix):
    WALL = '#'
    EMPTY = '.'
    ROBOT = '@'
    BOX = 'O'
    LBOX = '['
    RBOX = ']'

    def __init__(self, matrix, instructions, start_x, start_y):
        super().__init__(matrix, start_x, start_y)
        self.instructions = instructions
        self.box_locations = self.get_box_locations()
        # Initialize the visualization
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.im = None

    def setup_animation(self):
        # Create a color map for different symbols with specific colors
        self.symbol_map = {
            self.WALL: ('Wall', 'gray'),
            self.EMPTY: ('Empty', 'white'),
            self.ROBOT: ('Robot', 'red'),
            self.LBOX: ('Box', 'blue'),
            self.RBOX: ('Box', 'blue')
        }
        # Create numeric mapping for visualization
        self.symbol_to_num = {symbol: i for i, symbol in enumerate(self.symbol_map.keys())}

        # Convert matrix to numeric array for visualization
        numeric_matrix = [[self.symbol_to_num[symbol] for symbol in row] 
                         for row in self.matrix]
        
        # Set up the plot
        self.im = self.ax.imshow(numeric_matrix, cmap='Set3')
        self.ax.grid(False)
        self.ax.set_xticks(range(self.width))
        self.ax.set_yticks(range(self.height))
        

        # Create legend handles
        legend_elements = [
            plt.Rectangle((0, 0), 1, 1, facecolor=color, label=label)
            for label, color in self.symbol_map.values()
        ]
        
        # Add legend
        self.ax.legend(handles=legend_elements, 
                    loc='center left',  # Position legend outside the plot
                    bbox_to_anchor=(1, 0.5))
        
        # Adjust layout to prevent legend overlap
        plt.tight_layout()
        return self.im,

    
    def run_with_animation(self):
        """Run the simulation with live visualization"""
        self.setup_animation()
        
        for instruction in self.instructions:
            self.move(instruction)
            # Force drawing update
            numeric_matrix = [[self.symbol_to_num[symbol] for symbol in row] 
                            for row in self.matrix]
            self.im.set_array(numeric_matrix)
            plt.pause(0.1)  # Pause to show movement
        
        plt.show()

    def move(self, direction):
        '''
        move into one of the available directions UP, DOWN, RIGHT, LEFT.
        if the space is empty, the robot moves in that direction.
        if the space is occupied by a box, try to move the box. Multiple boxes in a row can be moved as long as there is an empty space after the last box. If there is a wall after the last box, it cannot move. When the boxes are moved, the robot also moves in the direction, otherwise it stays
        if the space is a wall, the robot cannot move and remains where they are.
    
        return the new position if in bounds, (-1, -1) if the chosen direction is out of bounds
        '''
        new_position = (self.position[0] + direction[0], self.position[1] + direction[1])
        if self.is_out_of_bounds(new_position):
            return (-1, -1)
        # moving to a wall
        elif self.get(new_position[0], new_position[1]) == self.WALL:
            return self.position
        # moving to an empty space
        elif self.get(new_position[0], new_position[1]) == self.EMPTY:
            self.set(self.position[0], self.position[1], self.EMPTY)
            self.position = new_position
            self.set(self.position[0], self.position[1], self.ROBOT)
            return self.position
        # moving to a box
        elif self.get(new_position[0], new_position[1]) in (self.LBOX, self.RBOX):
            # Find all the positions beyond connected boxes. If any of them are a wall, they block any movement.
            # if all are empty, all the boxes move one step in the direction 
            affected_boxes = self.get_box_closure(new_position, direction)
            if self.can_move(affected_boxes, direction):
                self.move_boxes(affected_boxes, direction)
                self.set(self.position[0], self.position[1], self.EMPTY)
                self.position = new_position
                self.set(self.position[0], self.position[1], self.ROBOT)
            return self.position
        else:
            return self.position

    def get_box_closure(self, position, direction):
        if self.get(position[0], position[1]) not in (self.BOX, self.LBOX, self.RBOX):
            return []
        else:
            box_closure = []
            # only store the left part of the box
            if self.get(position[0], position[1]) == self.RBOX:
                position = (position[0] - 1, position[1])
            box_queue = [position]
            while len(box_queue) > 0:
                current_box = box_queue.pop(0)
                box_closure.append(current_box)
                neighbors = []
                if direction in (self.UP, self.DOWN):
                    neighbors = [(current_box[0], current_box[1]+direction[1]), (current_box[0]+1, current_box[1]+direction[1]) ]
                elif direction == self.LEFT:
                    neighbors = [(current_box[0]+direction[0], current_box[1])]
                elif direction == self.RIGHT:
                    neighbors = [(current_box[0]+1+direction[0], current_box[1])]
                else:
                    print(f'Error: unexpected direction: {direction} in calculating box closure for {current_box}')
                    return []
                for neighbor in neighbors:
                    if self.get(neighbor[0], neighbor[1]) == self.LBOX and neighbor not in box_closure and neighbor not in box_queue:
                        box_queue.append(neighbor)
                    elif self.get(neighbor[0], neighbor[1]) == self.RBOX and (neighbor[0]-1, neighbor[1]) not in box_closure and (neighbor[0]-1, neighbor[1]) not in box_queue:
                        box_queue.append((neighbor[0]-1, neighbor[1]))
            return box_closure
        
    def can_move(self, box_closure, direction):
        for box in box_closure:
            if direction in (self.UP, self.DOWN):
                if self.get(box[0], box[1]+direction[1]) == self.WALL or self.get(box[0]+1, box[1]+direction[1]) == self.WALL:
                    return False
            elif direction == self.LEFT:
                if self.get(box[0]+direction[0], box[1]) == self.WALL:
                    return False
            elif direction == self.RIGHT:
                if self.get(box[0]+direction[0]+1, box[1]) == self.WALL:
                    return False
            else:
                print(f'Error: unexpected direction: {direction}')
                return False
        return True

    def move_boxes(self, box_closure, direction):
        '''
        move all boxes in the given direction
        '''
        if self.can_move(box_closure, direction):
            # first mark all locations as empty
            for box in box_closure:
                self.set(box[0], box[1], self.EMPTY)
                self.set(box[0]+1, box[1], self.EMPTY)
            # now move all of them in direction
            for box in box_closure:
                self.set(box[0] + direction[0], box[1] + direction[1], self.LBOX)
                self.set(box[0] + direction[0] + 1, box[1] + direction[1], self.RBOX)
        else:
            print(f'Error: cannot move boxes in direction: {direction}')
            return (-1, -1)

    def get_box_gps(self):
        '''
        get the sum of all boxes' GPS coordinates
        '''
        gps = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.get(x, y) == self.LBOX:
                    gps += 100 * y + x
        return gps

    def get_box_locations(self):
        '''
        get the locations of all boxes
        '''
        box_locations = []
        for y in range(self.height):
            for x in range(self.width):
                if self.get(x, y) == self.LBOX:
                    box_locations.append((x, y))
        return box_locations

    @classmethod
    def from_inputfile(cls, inputfile):
        matrix = []
        instructions = []
        instruction_map = {'^': cls.UP, 'v': cls.DOWN, '<': cls.LEFT, '>': cls.RIGHT}
        start_x, start_y = 0, 0
        line_count = 0
        with open(inputfile) as f:
            line_count = 0
            for line in f.readlines():
                if line.startswith(cls.WALL):
                    row = []
                    for char in line.strip():
                        if char == cls.BOX:
                            row.append(cls.LBOX)
                            row.append(cls.RBOX)
                        elif char == cls.ROBOT:
                            row.append(cls.ROBOT)
                            row.append(cls.EMPTY)
                            start_x = row.index(cls.ROBOT)
                            start_y = line_count
                        else:
                            row.append(char)
                            row.append(char)
                    matrix.append(row)
                    line_count += 1
                elif line[0] in ('<', '^', '>', 'v'):
                    instructions.extend([instruction_map[c] for c in line if c in ('<', '^', '>', 'v')])
                else:
                    continue # don't read empty lines
        return cls(matrix, instructions, start_x, start_y)

if __name__ == '__main__':
    main()