'''
--- Part Two ---

While The Historians begin working around the guard's patrol route, you borrow their fancy device and step outside the lab. From the safety of a supply closet, you time travel through the last few months and record the nightly status of the lab's guard post on the walls of the closet.

Returning after what seems like only a few seconds to The Historians, they explain that the guard's patrol area is simply too large for them to safely search the lab without getting caught.

Fortunately, they are pretty sure that adding a single new obstruction won't cause a time paradox. They'd like to place the new obstruction in such a way that the guard will get stuck in a loop, making the rest of the lab safe to search.

To have the lowest chance of creating a time paradox, The Historians would like to know all of the possible positions for such an obstruction. The new obstruction can't be placed at the guard's starting position - the guard is there right now and would notice.

In the above example, there are only 6 different positions where a new obstruction would cause the guard to get stuck in a loop. The diagrams of these six situations use O to mark the new obstruction, | to show a position where the guard moves up/down, - to show a position where the guard moves left/right, and + to show a position where the guard moves both up/down and left/right.

Option one, put a printing press next to the guard's starting position:

....#.....
....+---+#
....|...|.
..#.|...|.
....|..#|.
....|...|.
.#.O^---+.
........#.
#.........
......#...

Option two, put a stack of failed suit prototypes in the bottom right quadrant of the mapped area:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
......O.#.
#.........
......#...

Option three, put a crate of chimney-squeeze prototype fabric next to the standing desk in the bottom right quadrant:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
.+----+O#.
#+----+...
......#...

Option four, put an alchemical retroencabulator near the bottom left corner:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
..|...|.#.
#O+---+...
......#...

Option five, put the alchemical retroencabulator a bit to the right instead:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
....|.|.#.
#..O+-+...
......#...

Option six, put a tank of sovereign glue right next to the tank of universal solvent:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
.+----++#.
#+----++..
......#O..

It doesn't really matter what you choose to use as an obstacle so long as you and The Historians can put it into position without the guard noticing. The important thing is having enough options that you can find one that minimizes time paradoxes, and in this example, there are 6 different positions you could choose.

You need to get the guard stuck in a loop by adding a single new obstruction. How many different positions could you choose for this obstruction?

'''
from copy import deepcopy

class Map:

    UP = (0, -1)
    DOWN = (0, 1)
    RIGHT = (1, 0)
    LEFT = (-1, 0)

    def __init__(self, map, starting_pos, obstacle_pos=None):
        self.map = deepcopy(map)
        self.position = starting_pos
        self.direction = self.UP
        self.visited_locations = set()
        self.start_position = starting_pos
        self.map[starting_pos[1]][starting_pos[0]] = '.'
        if obstacle_pos:
            self.map[obstacle_pos[1]][obstacle_pos[0]] = '#'

    @classmethod
    def from_inputfile(cls, inputfile):
        map = []
        starting_pos = None
        with open(inputfile) as f:
            for line in f.readlines():
                map.append([char for char in line.strip()])
                if '^' in line:
                    starting_pos = (line.find('^'), len(map)-1)
        return cls(map, starting_pos)
    
    def rotate_direction(self, direction):
        if direction == self.UP:
            return self.RIGHT
        elif direction == self.RIGHT:
            return self.DOWN
        elif direction == self.DOWN:
            return self.LEFT
        elif direction == self.LEFT:
            return self.UP
        else:
            print("Error - invalid direction")
            return (-1, -1)

    def is_out_of_bounds(self, position):
        return position[0] < 0 or position[0] >= len(self.map[0]) or position[1] < 0 or position[1] >= len(self.map)
    
    def move(self, direction):
        '''
        move into one of the available directions UP, DOWN, RIGHT, LEFT.
        return the new position if the field in the chosen directory is empty ('.')
        return the same position if there is an obstacle in the chosen direction ('#')
        return (-1, -1) if the chosen direction is out of bounds
        '''
        new_position = (self.position[0] + direction[0], self.position[1] + direction[1])
        if self.is_out_of_bounds(new_position):
            return ((-1, -1), self.direction)
        elif self.map[new_position[1]][new_position[0]] == '#':
            self.direction = self.rotate_direction(self.direction)
            return (self.position, self.direction)
        elif self.map[new_position[1]][new_position[0]] == '.':
            self.position = new_position
            return (self.position, self.direction)
        else:
            print("Error - hit something unexpected at location " + str(new_position))
            return ((-1, -1), self.direction)

    def is_loop(self):
        self.visited_locations.add((self.position, self.direction))
        looping = False
        while not looping:
            (new_pos, new_dir) = self.move(self.direction)
            if new_pos == (-1, -1):
                return False
            elif (new_pos, new_dir) in self.visited_locations:
                print("loop discovered at " + str((new_pos, new_dir)))
                return True
            else:
                print("moving to " + str((new_pos, new_dir)) + " checking " + str((self.position, self.direction)))
                self.visited_locations.add((new_pos, new_dir))
        return False

def main():
    inputfile = "data/aoc24_input_06.txt"
#    inputfile = "data/test_06.txt"
    map = Map.from_inputfile(inputfile)
    loops = 0
    if map.is_loop():
        print("Loop detected")
    else:
        locations = set([x[0] for x in map.visited_locations])
        print("Maximum locations " + str(len(locations)))
        print("Starting position: " + str(map.start_position))
        for location in locations:
            if location == map.start_position:
                continue
            new_map = Map(map.map, map.start_position, location)
            if new_map.is_loop():
                loops += 1
            else:
                continue
        print("Number of loops: " + str(loops))


if __name__ == '__main__':
    main()