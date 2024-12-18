'''
--- Day 16: Reindeer Maze ---

It's time again for the Reindeer Olympics! This year, the big event is the Reindeer Maze, where the Reindeer compete for the lowest score.

You and The Historians arrive to search for the Chief right as the event is about to start. It wouldn't hurt to watch a little, right?

The Reindeer start on the Start Tile (marked S) facing East and need to reach the End Tile (marked E). They can move forward one tile at a time (increasing their score by 1 point), but never into a wall (#). They can also rotate clockwise or counterclockwise 90 degrees at a time (increasing their score by 1000 points).

To figure out the best place to sit, you start by grabbing a map (your puzzle input) from a nearby kiosk. For example:

###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############

There are many paths through this maze, but taking any of the best paths would incur a score of only 7036. This can be achieved by taking a total of 36 steps forward and turning 90 degrees a total of 7 times:


###############
#.......#....E#
#.#.###.#.###^#
#.....#.#...#^#
#.###.#####.#^#
#.#.#.......#^#
#.#.#####.###^#
#..>>>>>>>>v#^#
###^#.#####v#^#
#>>^#.....#v#^#
#^#.#.###.#v#^#
#^....#...#v#^#
#^###.#.#.#v#^#
#S..#.....#>>^#
###############

Here's a second example:

#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################

In this maze, the best paths cost 11048 points; following one such path would look like this:

#################
#...#...#...#..E#
#.#.#.#.#.#.#.#^#
#.#.#.#...#...#^#
#.#.#.#.###.#.#^#
#>>v#.#.#.....#^#
#^#v#.#.#.#####^#
#^#v..#.#.#>>>>^#
#^#v#####.#^###.#
#^#v#..>>>>^#...#
#^#v###^#####.###
#^#v#>>^#.....#.#
#^#v#^#####.###.#
#^#v#^........#.#
#^#v#^#########.#
#S#>>^..........#
#################

Note that the path shown above includes one 90 degree turn as the very first move, rotating the Reindeer from facing East to facing North.

Analyze your map carefully. What is the lowest score a Reindeer could possibly get?
'''

from matrix import Matrix
from priorityqueue import PriorityQueue

def main():
    maze = Maze.from_inputfile('data/aoc24_input_16.txt')
#    maze = Maze.from_inputfile('data/test16.txt')
    maze.find_shortest_path()
    maze.visualize()

class Maze(Matrix):
    WALL = '#'
    EMPTY = '.'
    START = 'S'
    END = 'E'

    def __init__(self, matrix, start_pos_x, start_pos_y, end_pos_x, end_pos_y, direction):
        super().__init__(matrix, start_pos_x, start_pos_y, direction)
        self.end_pos = (end_pos_x, end_pos_y)
        self.start_pos = (start_pos_x, start_pos_y)
        self.visited = dict() # mapping each visited node to its lowest distance
        self.score = 0
        self.path = []

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
        return cls(matrix, start_pos_x, start_pos_y, end_pos_x, end_pos_y, Matrix.RIGHT)

    def find_shortest_path(self):
        '''
        find the shortest path from start to end
        '''
        queue = PriorityQueue()
        queue.push((self.start_pos, self.RIGHT, None, None, 0), 0) # start with the start node location, None as predecessor, and 0 as distance
        while not queue.is_empty():
            current_node, current_direction, predecessor, predecessor_direction, distance = queue.pop()
            if current_node in self.visited and self.visited[current_node] <= distance:
                # we have already visited this node with a lower or equal distance, so we can skip it
                continue
            elif current_node == self.end_pos:
                # we have reached the end node, so we can stop
                self.visited[current_node] = distance
                print(f"Found end node {current_node} with distance {distance}")
                break
            else:
                self.visited[current_node] = distance
                neighbors = [neighbor for neighbor in self.get_neighbors(current_node[0],current_node[1])]
                for neighbor in neighbors:
                    if self.get(neighbor[0], neighbor[1]) == self.WALL:
                        continue
                    elif neighbor == predecessor:
                        # we have already visited this node with the same direction, so we can skip it
                        continue
                    elif neighbor[0] == current_direction[0]+current_node[0] and neighbor[1] == current_direction[1]+current_node[1]:
                        print(f'moving straight to {neighbor}')
                        # moving in the same direction. Cost is 1
                        queue.push((neighbor, current_direction, current_node, current_direction, distance+1), distance + 1)
                    else: # we need to make a turn
                        print(f'moving after turning to {neighbor}')
                        new_direction = (neighbor[0] - current_node[0],  neighbor[1] - current_node[1])
                        # moving in the opposite direction. Cost is 1001 (1000 for turning, 1 for moving)
                        queue.push((neighbor, new_direction, current_node, current_direction, distance+1001), distance + 1001) 
        return self.visited[self.end_pos]

if __name__ == '__main__':
    main()