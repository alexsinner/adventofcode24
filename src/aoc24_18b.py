'''
--- Part Two ---

The Historians aren't as used to moving around in this pixelated universe as you are. You're afraid they're not going to be fast enough to make it to the exit before the path is completely blocked.

To determine how fast everyone needs to go, you need to determine the first byte that will cut off the path to the exit.

In the above example, after the byte at 1,1 falls, there is still a path to the exit:

O..#OOO
O##OO#O
O#OO#OO
OOO#OO#
###OO##
.##O###
#.#OOOO

However, after adding the very next byte (at 6,1), there is no longer a path to the exit:

...#...
.##..##
.#..#..
...#..#
###..##
.##.###
#.#....

So, in this example, the coordinates of the first byte that prevents the exit from being reachable are 6,1.

Simulate more of the bytes that are about to corrupt your memory space. What are the coordinates of the first byte that will prevent the exit from being reachable from your starting position? (Provide the answer as two integers separated by a comma with no other characters.)
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

    def get_reachable_tiles(self):
        tiles = set()
        queue = [self.start_pos]
        while len(queue) > 0:
            current_node = queue.pop()
            neighbors = [neighbor for neighbor in self.get_neighbors(current_node[0], current_node[1])]
            for neighbor in neighbors:
                if neighbor in tiles:
                    continue
                elif self.get(neighbor[0], neighbor[1]) == self.CORRUPTED:
                    continue
                else:
                    tiles.add(neighbor)
                    queue.append(neighbor)
        return tiles

    def find_path_blocking_tile(self):
        for i, falling_byte in enumerate(self.falling_bytes):
            self.matrix[falling_byte[1]][falling_byte[0]] = MemoryMap.CORRUPTED
            print(f'{i}: {falling_byte}')
            reachable_tiles = self.get_reachable_tiles()
            if self.end_pos not in reachable_tiles:
                return falling_byte
        return (-1, -1) # if we do not find a blocking tile
    
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
#    memory_map = MemoryMap(7, 7, 0, 0, 6, 6, MemoryMap.falling_bytes_from_inputfile('data/test18.txt'))
    print(memory_map.find_path_blocking_tile())
    memory_map.visualize()


if __name__ == '__main__':
    main()