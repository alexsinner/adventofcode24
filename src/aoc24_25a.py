'''
--- Day 25: Code Chronicle ---

Out of ideas and time, The Historians agree that they should go back to check the Chief Historian's office one last time, just in case he went back there without you noticing.

When you get there, you are surprised to discover that the door to his office is locked! You can hear someone inside, but knocking yields no response. The locks on this floor are all fancy, expensive, virtual versions of five-pin tumbler locks, so you contact North Pole security to see if they can help open the door.

Unfortunately, they've lost track of which locks are installed and which keys go with them, so the best they can do is send over schematics of every lock and every key for the floor you're on (your puzzle input).

The schematics are in a cryptic file format, but they do contain manufacturer information, so you look up their support number.

"Our Virtual Five-Pin Tumbler product? That's our most expensive model! Way more secure than--" You explain that you need to open a door and don't have a lot of time.

"Well, you can't know whether a key opens a lock without actually trying the key in the lock (due to quantum hidden variables), but you can rule out some of the key/lock combinations."

"The virtual system is complicated, but part of it really is a crude simulation of a five-pin tumbler lock, mostly for marketing reasons. If you look at the schematics, you can figure out whether a key could possibly fit in a lock."

He transmits you some example schematics:

#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####

"The locks are schematics that have the top row filled (#) and the bottom row empty (.); the keys have the top row empty and the bottom row filled. If you look closely, you'll see that each schematic is actually a set of columns of various heights, either extending downward from the top (for locks) or upward from the bottom (for keys)."

"For locks, those are the pins themselves; you can convert the pins in schematics to a list of heights, one per column. For keys, the columns make up the shape of the key where it aligns with pins; those can also be converted to a list of heights."

"So, you could say the first lock has pin heights 0,5,3,4,3:"

#####
.####
.####
.####
.#.#.
.#...
.....

"Or, that the first key has heights 5,0,2,1,3:"

.....
#....
#....
#...#
#.#.#
#.###
#####

"These seem like they should fit together; in the first four columns, the pins and key don't overlap. However, this key cannot be for this lock: in the rightmost column, the lock's pin overlaps with the key, which you know because in that column the sum of the lock height and key height is more than the available space."

"So anyway, you can narrow down the keys you'd need to try by just testing each key with each lock, which means you would have to check... wait, you have how many locks? But the only installation that size is at the North--" You disconnect the call.

In this example, converting both locks to pin heights produces:

0,5,3,4,3
1,2,0,5,3

Converting all three keys to heights produces:

5,0,2,1,3
4,3,4,0,2
3,0,2,0,1

Then, you can try every key with every lock:

    Lock 0,5,3,4,3 and key 5,0,2,1,3: overlap in the last column.
    Lock 0,5,3,4,3 and key 4,3,4,0,2: overlap in the second column.
    Lock 0,5,3,4,3 and key 3,0,2,0,1: all columns fit!
    Lock 1,2,0,5,3 and key 5,0,2,1,3: overlap in the first column.
    Lock 1,2,0,5,3 and key 4,3,4,0,2: all columns fit!
    Lock 1,2,0,5,3 and key 3,0,2,0,1: all columns fit!

So, in this example, the number of unique lock/key pairs that fit together without overlapping in any column is 3.

Analyze your lock and key schematics. How many unique lock/key pairs fit together without overlapping in any column?
'''

class Lock():

    def __init__(self, combination, size):
        self.combination = combination
        self.size = size
        self.matching_keys = []

    @classmethod
    def from_matrix(cls, matrix):
        combination = [0] * len(matrix[0])
        if matrix[0][0] == '.':
            print('Not a lock matrix') # type: ignore
            return None
        for row in matrix[1:-1]: #ignore first and last row
            for i in range(len(matrix[0])):
                if row[i] == '#':
                    combination[i] += 1
        return cls(tuple(combination), len(matrix)-2)

class Key():
    def __init__(self, combination, size):
        self.combination = combination
        self.size = size
        self.matching_locks = []

    @classmethod
    def from_matrix(cls, matrix):
        combination = [0] * len(matrix[0])
        if matrix[0][0] == '#':
            print('Not a key matrix') # type: ignore
            return None
        for row in matrix[1:-1]: #ignore first and last row
            for i in range(len(matrix[0])):
                if row[i] == '#':
                    combination[i] += 1
        return cls(tuple(combination), len(matrix)-2)
    
    def matches_lock(self, lock:Lock):
        for i in range(len(self.combination)):
            if self.combination[i] + lock.combination[i] > lock.size:
                return False
        if lock not in self.matching_locks:
            self.matching_locks.append(lock)
        if self not in lock.matching_keys:
            lock.matching_keys.append(self)
        return True
    
def parse_input_file(inputfile):
    # make sure to add a newline to the inputfile to read all locks! (sorry, lazy to fix that edge case)
    keys = []
    locks = []
    with open(inputfile) as f:
        new_matrix = True
        for line in f.readlines():
            if new_matrix:
                matrix = []
                new_matrix = False
            if line.strip() == '':
                new_matrix = True
                if matrix[0][0] == '.':
                    keys.append(Key.from_matrix(matrix))
                elif matrix[0][0] == '#':
                    locks.append(Lock.from_matrix(matrix))
            else:
                matrix.append([c for c in line.strip()])
    return keys, locks

def main():
    inputfile = 'data/aoc24_input_25.txt'
    keys, locks = parse_input_file(inputfile)
    for key in keys:
        for lock in locks:
            key.matches_lock(lock)
    total = 0
    for key in keys:
        total += len(key.matching_locks)
    print(f'total: {total}')

if __name__ == '__main__':
    main()