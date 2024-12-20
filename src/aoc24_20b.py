'''--- Part Two ---

The programs seem perplexed by your list of cheats. Apparently, the two-picosecond cheating rule was deprecated several milliseconds ago! The latest version of the cheating rule permits a single cheat that instead lasts at most 20 picoseconds.

Now, in addition to all the cheats that were possible in just two picoseconds, many more cheats are possible. This six-picosecond cheat saves 76 picoseconds:

###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#1#####.#.#.###
#2#####.#.#...#
#3#####.#.###.#
#456.E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############

Because this cheat has the same start and end positions as the one above, it's the same cheat, even though the path taken during the cheat is different:

###############
#...#...#.....#
#.#.#.#.#.###.#
#S12..#.#.#...#
###3###.#.#.###
###4###.#.#...#
###5###.#.###.#
###6.E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############

Cheats don't need to use all 20 picoseconds; cheats can last any amount of time up to and including 20 picoseconds (but can still only end when the program is on normal track). Any cheat time not used is lost; it can't be saved for another cheat later.

You'll still need a list of the best cheats, but now there are even more to choose between. Here are the quantities of cheats in this example that save 50 picoseconds or more:

    There are 32 cheats that save 50 picoseconds.
    There are 31 cheats that save 52 picoseconds.
    There are 29 cheats that save 54 picoseconds.
    There are 39 cheats that save 56 picoseconds.
    There are 25 cheats that save 58 picoseconds.
    There are 23 cheats that save 60 picoseconds.
    There are 20 cheats that save 62 picoseconds.
    There are 19 cheats that save 64 picoseconds.
    There are 12 cheats that save 66 picoseconds.
    There are 14 cheats that save 68 picoseconds.
    There are 12 cheats that save 70 picoseconds.
    There are 22 cheats that save 72 picoseconds.
    There are 4 cheats that save 74 picoseconds.
    There are 3 cheats that save 76 picoseconds.

Find the best cheats using the updated cheating rules. How many cheats would save you at least 100 picoseconds?
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
        path.append(start)
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

    def get_absolute_distance(self, pos_a, pos_b):
        return abs(pos_a[0] - pos_b[0]) + abs(pos_a[1] - pos_b[1])

    def get_cheat_paths(self):
        '''get all the cheat paths saving more than 100 picoseconds given a node on the path from which we take a 20 ps shortcut'''
        cheat_paths = 0
        for i, position in enumerate(self.track_path):  # iterate over all nodes on the path
            for j in range(len(self.track_path)-1,  i, -1):  # iterate from the back of the list
                distance = self.get_absolute_distance(position, self.track_path[j])
                # print(f'comparing distance from {position} to {self.track_path[j]}: {distance}')
                if distance <= 20:
                    cheat_length = (i) + (distance) + (self.track_length - j) # distance to the node where the cheat is activated + distance to node + distance to end node 
                    delta = self.track_length - cheat_length
                    # print(f'cheat length: {cheat_length} delta {delta}')
                    if self.track_length - cheat_length >= 100:
                        cheat_paths += 1
        return cheat_paths

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
    print(f'Number of cheats saving more than 100 picoseconds: {racemap.get_cheat_paths()}')

if __name__ == '__main__':
    main()
