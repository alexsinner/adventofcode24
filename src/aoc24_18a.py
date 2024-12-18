'''
--- Day 18: RAM Run ---

You and The Historians look a lot more pixelated than you remember. You're inside a computer at the North Pole!

Just as you're about to check out your surroundings, a program runs up to you. "This region of memory isn't safe! The User misunderstood what a pushdown automaton is and their algorithm is pushing whole bytes down on top of us! Run!"

The algorithm is fast - it's going to cause a byte to fall into your memory space once every nanosecond! Fortunately, you're faster, and by quickly scanning the algorithm, you create a list of which bytes will fall (your puzzle input) in the order they'll land in your memory space.

Your memory space is a two-dimensional grid with coordinates that range from 0 to 70 both horizontally and vertically. However, for the sake of example, suppose you're on a smaller grid with coordinates that range from 0 to 6 and the following list of incoming byte positions:

5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0

Each byte position is given as an X,Y coordinate, where X is the distance from the left edge of your memory space and Y is the distance from the top edge of your memory space.

You and The Historians are currently in the top left corner of the memory space (at 0,0) and need to reach the exit in the bottom right corner (at 70,70 in your memory space, but at 6,6 in this example). You'll need to simulate the falling bytes to plan out where it will be safe to run; for now, simulate just the first few bytes falling into your memory space.

As bytes fall into your memory space, they make that coordinate corrupted. Corrupted memory coordinates cannot be entered by you or The Historians, so you'll need to plan your route carefully. You also cannot leave the boundaries of the memory space; your only hope is to reach the exit.

In the above example, if you were to draw the memory space after the first 12 bytes have fallen (using . for safe and # for corrupted), it would look like this:

...#...
..#..#.
....#..
...#..#
..#..#.
.#..#..
#.#....

You can take steps up, down, left, or right. After just 12 bytes have corrupted locations in your memory space, the shortest path from the top left corner to the exit would take 22 steps. Here (marked with O) is one such path:

OO.#OOO
.O#OO#O
.OOO#OO
...#OO#
..#OO#.
.#.O#..
#.#OOOO

Simulate the first kilobyte (1024 bytes) falling onto your memory space. Afterward, what is the minimum number of steps needed to reach the exit?
'''


from matrix import Matrix
from priorityqueue import PriorityQueue

class MemoryMap(Matrix):
    EMPTY = '.'
    CORRUPTED = '#'

    def __init__(self, x_size, y_size, start_pos_x, start_pos_y, end_pos_x, end_pos_y, falling_bytes):
        self.falling_bytes = falling_bytes
        self.start_pos = (start_pos_x, start_pos_y)
        self.end_pos = (end_pos_x, end_pos_y)
        matrix = [[MemoryMap.EMPTY for _ in range(x_size)] for _ in range(y_size)]
        super().__init__(matrix, start_pos_x, start_pos_y)
        self.visited = dict() # mapping each visited node to its lowest distance

    @classmethod
    def falling_bytes_from_inputfile(cls,inputfile):
        falling_bytes = []
        with open(inputfile) as f:
            for line in f.readlines():
                falling_bytes.append(tuple(map(int, line.strip().split(','))))
        return falling_bytes
    
    def apply_falling_bytes(self, amount):
        for falling_byte in self.falling_bytes[:amount]:
            self.matrix[falling_byte[1]][falling_byte[0]] = MemoryMap.CORRUPTED

    def find_shortest_path(self):
        '''
        find the shortest path from start to end
        '''
        queue = PriorityQueue()
        queue.push((self.start_pos, None, 0), 0) # start with the start node location, None as predecessor, and 0 as distance
        while not queue.is_empty():
            current_node, predecessor, distance = queue.pop()
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
                    if self.get(neighbor[0], neighbor[1]) == self.CORRUPTED:
                        continue
                    elif neighbor == predecessor:
                        # we have already visited this node with the same direction, so we can skip it
                        continue
                    else:
                        # moving to neighbor. Cost is 1
                        queue.push((neighbor, current_node, distance+1), distance + 1)
        return self.visited[self.end_pos]
    
def main():
    memory_map = MemoryMap(71, 71, 0, 0, 70, 70, MemoryMap.falling_bytes_from_inputfile('data/aoc24_input_18.txt'))
    memory_map.apply_falling_bytes(1024)
    memory_map.find_shortest_path()
    memory_map.visualize()


if __name__ == '__main__':
    main()