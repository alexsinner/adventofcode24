'''
--- Part Two ---

Watching over your shoulder as you work, one of The Historians asks if you took the effects of resonant harmonics into your calculations.

Whoops!

After updating your model, it turns out that an antinode occurs at any grid position exactly in line with at least two antennas of the same frequency, regardless of distance. This means that some of the new antinodes will occur at the position of each antenna (unless that antenna is the only one of its frequency).

So, these three T-frequency antennas now create many antinodes:

T....#....
...T......
.T....#...
.........#
..#.......
..........
...#......
..........
....#.....
..........

In fact, the three T-frequency antennas are all exactly in line with two antennas, so they are all also antinodes! This brings the total number of antinodes in the above example to 9.

The original example now has 34 antinodes, including the antinodes that appear on every antenna:

##....#....#
.#.#....0...
..#.#0....#.
..##...0....
....0....#..
.#...#A....#
...#..#.....
#....#.#....
..#.....A...
....#....A..
.#........#.
...#......##

Calculate the impact of the signal using this updated model. How many unique locations within the bounds of the map contain an antinode?
'''

from matrix import Matrix

def main():
    inputfile = "data/aoc24_input_08.txt"
    antenna_map = Matrix.from_inputfile(inputfile)
    print(len(calculate_antinode_locations(antenna_map)))

def calculate_antinode_locations(antenna_map):
    antinode_locations = set()
    antennas = dict()
    # first create a dict mapping each frequency to locations with antennas with that frequency
    for y in range(antenna_map.height):
        for x in range(antenna_map.width):
            if antenna_map.get(x, y) == '.':
                continue
            else:
                if antenna_map.get(x, y) not in antennas:
                    antennas[antenna_map.get(x, y)] = [(x, y)]
                else:
                    antennas[antenna_map.get(x, y)].append((x, y))
    # now calculate all the antinode locations for each frequency
    for key in antennas:
        locations = [x for x in calculate_antinodes(antennas[key], antenna_map) if not antenna_map.is_out_of_bounds(x)]
        antinode_locations.update(locations)
    return antinode_locations

def calculate_antinodes(locationlist, antennamap):
    locations = set()
    for i in range(len(locationlist)):
        for j in range(i+1, len(locationlist)):
            x1, y1 = locationlist[i]
            x2, y2 = locationlist[j]
            delta = (x2 - x1, y2 - y1)
            locations.add((x1, y1))
            locations.add((x2, y2))
            while not antennamap.is_out_of_bounds((x1, y1)):
                x1 -= delta[0]
                y1 -= delta[1]
                locations.add((x1, y1))
            while not antennamap.is_out_of_bounds((x2, y2)):
                x2 += delta[0]
                y2 += delta[1]
                locations.add((x2, y2))
    return locations

if __name__ == '__main__':
    main()

