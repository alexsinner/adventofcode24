'''
--- Day 20: Race Condition ---

The Historians are quite pixelated again. This time, a massive, black building looms over you - you're right outside the CPU!

While The Historians get to work, a nearby program sees that you're idle and challenges you to a race. Apparently, you've arrived just in time for the frequently-held race condition festival!

The race takes place on a particularly long and twisting code path; programs compete to see who can finish in the fewest picoseconds. The winner even gets their very own mutex!

They hand you a map of the racetrack (your puzzle input). For example:

###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############

The map consists of track (.) - including the start (S) and end (E) positions (both of which also count as track) - and walls (#).

When a program runs through the racetrack, it starts at the start position. Then, it is allowed to move up, down, left, or right; each such move takes 1 picosecond. The goal is to reach the end position as quickly as possible. In this example racetrack, the fastest time is 84 picoseconds.

Because there is only a single path from the start to the end and the programs all go the same speed, the races used to be pretty boring. To make things more interesting, they introduced a new rule to the races: programs are allowed to cheat.

The rules for cheating are very strict. Exactly once during a race, a program may disable collision for up to 2 picoseconds. This allows the program to pass through walls as if they were regular track. At the end of the cheat, the program must be back on normal track again; otherwise, it will receive a segmentation fault and get disqualified.

So, a program could complete the course in 72 picoseconds (saving 12 picoseconds) by cheating for the two moves marked 1 and 2:

###############
#...#...12....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############

Or, a program could complete the course in 64 picoseconds (saving 20 picoseconds) by cheating for the two moves marked 1 and 2:

###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...12..#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############

This cheat saves 38 picoseconds:

###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.####1##.###
#...###.2.#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############

This cheat saves 64 picoseconds and takes the program directly to the end:

###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..21...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############

Each cheat has a distinct start position (the position where the cheat is activated, just before the first move that is allowed to go through walls) and end position; cheats are uniquely identified by their start position and end position.

In this example, the total number of cheats (grouped by the amount of time they save) are as follows:

    There are 14 cheats that save 2 picoseconds.
    There are 14 cheats that save 4 picoseconds.
    There are 2 cheats that save 6 picoseconds.
    There are 4 cheats that save 8 picoseconds.
    There are 2 cheats that save 10 picoseconds.
    There are 3 cheats that save 12 picoseconds.
    There is one cheat that saves 20 picoseconds.
    There is one cheat that saves 36 picoseconds.
    There is one cheat that saves 38 picoseconds.
    There is one cheat that saves 40 picoseconds.
    There is one cheat that saves 64 picoseconds.

You aren't sure what the conditions of the racetrack will be like, so to give yourself as many options as possible, you'll need a list of the best cheats. How many cheats would save you at least 100 picoseconds?
'''
from matrix import Matrix
from priorityqueue import PriorityQueue

class RaceMap(Matrix):

    EMPTY = '.'
    WALL = '#'
    START = 'S'
    END = 'E'
    CHEAT = '*'

    def __init__(self, matrix, start_pos, end_pos):
        super().__init__(matrix, start_pos[0], start_pos[1])
        self.start = start_pos
        self.end = end_pos
        self.track_path, self.track_length = self.get_shortest_path(self.start, self.end)

    def get_shortest_path(self, start, end):
        '''return the shortest path from start to end'''
        queue = PriorityQueue()
        queue.push((start, 0), 0)
        visited_from = dict()
        visited_from[start] = (start, 0)
        while not queue.is_empty():
            (current, distance) = queue.pop()
            if current in visited_from and visited_from[current][1] < distance:
                # the node we are exploring has already been visited with a lower distance
                continue
            elif current == end:
                # we have reached the end node, so we can stop
                break
            for neighbor in self.get_neighbors(current[0],current[1]):
                if neighbor in visited_from:
                    continue
                elif self.get(neighbor[0],neighbor[1]) == self.WALL:
                    continue
                else:
                    queue.push((neighbor, distance + 1), distance +1)
                    visited_from[neighbor] = (current, distance+1)
        if end not in visited_from:
            return None, 0
        path = []
        current = end
        while current != start:
            path.append(current)
            current = visited_from[current][0]
        return list(reversed(path)), visited_from[end][1]

    def get_cheat_path(self, start, cheat, end):
        '''return the shortest path from start to end, but only if it is a cheat path'''
        self.set(cheat[0], cheat[1], self.CHEAT)
        path_to_cheat, distance_to_cheat = self.get_shortest_path(start, cheat)
        self.set(cheat[0], cheat[1], self.WALL)
        if path_to_cheat is None:
            return None, 0
        else:
            path_from_cheat, distance_from_cheat = self.get_shortest_path(cheat, end)
            if path_from_cheat is None:
                return None, 0
            else:
                return path_to_cheat + path_from_cheat[1:], distance_to_cheat + distance_from_cheat

    def get_cheat_locations(self):
        '''return a list of all possible cheat locations'''
        cheat_locations = []
        for y in range(len(self.matrix)):
            for x in range(len(self.matrix[y])):
                if self.matrix[y][x] == self.WALL:
                    # check if we can cheat through this position
                    neighbors = [position for position in self.get_neighbors(x, y) if self.get(position[0], position[1]) != self.WALL]
                    if len(neighbors) >= 2:
                        cheat_locations.append((x, y))
        return cheat_locations

    @classmethod
    def from_inputfile(cls, inputfile):
        matrix = []
        start_pos_x, start_pos_y = 0, 0
        end_pos_x, end_pos_y = 0, 0
        with open(inputfile) as f:
            rownum = 0
            for line in f.readlines():
                row = [char for char in line.strip()]
                if cls.START in row:
                    start_pos_x = row.index(cls.START)
                    start_pos_y = rownum
                if cls.END in row:
                    end_pos_x = row.index(cls.END)
                    end_pos_y = rownum
                matrix.append(row)
                rownum += 1
        return cls(matrix, (start_pos_x, start_pos_y), (end_pos_x, end_pos_y))

def main():
    inputfile = 'data/aoc24_input_20.txt'
    racemap = RaceMap.from_inputfile(inputfile)
    total = 0
    for pos in racemap.get_cheat_locations():
        path, distance = racemap.get_cheat_path(racemap.start, pos, racemap.end)
        delta = racemap.track_length - distance
        print(f'cheat path from {racemap.start} to {pos} to {racemap.end} is {distance} long, {delta} shorter than the full path')
        if delta >= 100:
            total +=1
    print(f'total: {total}')

if __name__ == '__main__':
    main()
