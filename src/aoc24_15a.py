'''
--- Day 15: Warehouse Woes ---

You appear back inside your own mini submarine! Each Historian drives their mini submarine in a different direction; maybe the Chief has his own submarine down here somewhere as well?

You look up to see a vast school of lanternfish swimming past you. On closer inspection, they seem quite anxious, so you drive your mini submarine over to see if you can help.

Because lanternfish populations grow rapidly, they need a lot of food, and that food needs to be stored somewhere. That's why these lanternfish have built elaborate warehouse complexes operated by robots!

These lanternfish seem so anxious because they have lost control of the robot that operates one of their most important warehouses! It is currently running amok, pushing around boxes in the warehouse with no regard for lanternfish logistics or lanternfish inventory management strategies.

Right now, none of the lanternfish are brave enough to swim up to an unpredictable robot so they could shut it off. However, if you could anticipate the robot's movements, maybe they could find a safe option.

The lanternfish already have a map of the warehouse and a list of movements the robot will attempt to make (your puzzle input). The problem is that the movements will sometimes fail as boxes are shifted around, making the actual movements of the robot difficult to predict.

For example:

##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^

As the robot (@) attempts to move, if there are any boxes (O) in the way, the robot will also attempt to push those boxes. However, if this action would cause the robot or a box to move into a wall (#), nothing moves instead, including the robot. The initial positions of these are shown on the map at the top of the document the lanternfish gave you.

The rest of the document describes the moves (^ for up, v for down, < for left, > for right) that the robot will attempt to make, in order. (The moves form a single giant sequence; they are broken into multiple lines just to make copy-pasting easier. Newlines within the move sequence should be ignored.)

Here is a smaller example to get started:

########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<

Were the robot to attempt the given sequence of moves, it would push around the boxes as follows:

Initial state:
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move <:
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move ^:
########
#.@O.O.#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move ^:
########
#.@O.O.#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move >:
########
#..@OO.#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move >:
########
#...@OO#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move >:
########
#...@OO#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move v:
########
#....OO#
##..@..#
#...O..#
#.#.O..#
#...O..#
#...O..#
########

Move v:
########
#....OO#
##..@..#
#...O..#
#.#.O..#
#...O..#
#...O..#
########

Move <:
########
#....OO#
##.@...#
#...O..#
#.#.O..#
#...O..#
#...O..#
########

Move v:
########
#....OO#
##.....#
#..@O..#
#.#.O..#
#...O..#
#...O..#
########

Move >:
########
#....OO#
##.....#
#...@O.#
#.#.O..#
#...O..#
#...O..#
########

Move >:
########
#....OO#
##.....#
#....@O#
#.#.O..#
#...O..#
#...O..#
########

Move v:
########
#....OO#
##.....#
#.....O#
#.#.O@.#
#...O..#
#...O..#
########

Move <:
########
#....OO#
##.....#
#.....O#
#.#O@..#
#...O..#
#...O..#
########

Move <:
########
#....OO#
##.....#
#.....O#
#.#O@..#
#...O..#
#...O..#
########

The larger example has many more moves; after the robot has finished those moves, the warehouse would look like this:

##########
#.O.O.OOO#
#........#
#OO......#
#OO@.....#
#O#.....O#
#O.....OO#
#O.....OO#
#OO....OO#
##########

The lanternfish use their own custom Goods Positioning System (GPS for short) to track the locations of the boxes. The GPS coordinate of a box is equal to 100 times its distance from the top edge of the map plus its distance from the left edge of the map. (This process does not stop at wall tiles; measure all the way to the edges of the map.)

So, the box shown below has a distance of 1 from the top edge of the map and 4 from the left edge of the map, resulting in a GPS coordinate of 100 * 1 + 4 = 104.

#######
#...O..
#......

The lanternfish would like to know the sum of all boxes' GPS coordinates after the robot finishes moving. In the larger example, the sum of all boxes' GPS coordinates is 10092. In the smaller example, the sum is 2028.

Predict the motion of the robot and boxes in the warehouse. After the robot is finished moving, what is the sum of all boxes' GPS coordinates?
'''

from matrix import Matrix

def main():
    warehouse_map = WarehouseMap.from_inputfile('data/aoc24_input_15.txt')
    for instruction in warehouse_map.instructions:
        warehouse_map.move(instruction)
    print(warehouse_map.get_box_gps())
#    warehouse_map.visualize()

class WarehouseMap(Matrix):
    WALL = '#'
    EMPTY = '.'
    ROBOT = '@'
    BOX = 'O'

    def __init__(self, matrix, instructions, start_x, start_y):
        super().__init__(matrix, start_x, start_y)
        self.instructions = instructions

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
        elif self.get(new_position[0], new_position[1]) == self.BOX:
            # First find the last box in the row
            last_box = new_position
            while self.get(last_box[0] + direction[0], last_box[1] + direction[1]) == self.BOX:
                last_box = (last_box[0] + direction[0], last_box[1] + direction[1])
            # box row ending in a wall and cannot be moved
            if self.get(last_box[0] + direction[0], last_box[1] + direction[1]) == self.WALL:
                return self.position
            # box row ending in an empty space => Robot moves into the first box space, box is moved to the empty space at end of row
            elif self.get(last_box[0] + direction[0], last_box[1] + direction[1]) == self.EMPTY:
                # the box can be moved
                self.set(last_box[0] + direction[0], last_box[1] + direction[1], self.BOX)
                self.set(self.position[0], self.position[1], self.EMPTY)
                self.position = new_position
                self.set(self.position[0], self.position[1], self.ROBOT)
                return self.position
            else:
                print(f'Error: unexpected object at the end of a box row: {self.get(last_box[0] + direction[0], last_box[1] + direction[1])}')
                return (-1, -1)
        else:
            print(f'Error: unexpected object: {self.get(new_position[0], new_position[1])}')
            return (-1, -1)
        
    def get_box_gps(self):
        '''
        get the sum of all boxes' GPS coordinates
        '''
        gps = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.get(x, y) == self.BOX:
                    gps += 100 * y + x
        return gps

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
                    matrix.append([char for char in line.strip()])
                    if cls.ROBOT in line:
                        start_x = line.index(cls.ROBOT)
                        start_y = line_count
                    line_count += 1
                elif line[0] in ('<', '^', '>', 'v'):
                    instructions.extend([instruction_map[c] for c in line if c in ('<', '^', '>', 'v')])
                else:
                    continue # don't read empty lines
        return cls(matrix, instructions, start_x, start_y)

if __name__ == '__main__':
    main()