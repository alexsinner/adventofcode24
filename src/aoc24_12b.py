'''
--- Part Two ---

Fortunately, the Elves are trying to order so much fence that they qualify for a bulk discount!

Under the bulk discount, instead of using the perimeter to calculate the price, you need to use the number of sides each region has. Each straight section of fence counts as a side, regardless of how long it is.

Consider this example again:

AAAA
BBCD
BBCC
EEEC

The region containing type A plants has 4 sides, as does each of the regions containing plants of type B, D, and E. However, the more complex region containing the plants of type C has 8 sides!

Using the new method of calculating the per-region price by multiplying the region's area by its number of sides, regions A through E have prices 16, 16, 32, 4, and 12, respectively, for a total price of 80.

The second example above (full of type X and O plants) would have a total price of 436.

Here's a map that includes an E-shaped region full of type E plants:

EEEEE
EXXXX
EEEEE
EXXXX
EEEEE

The E-shaped region has an area of 17 and 12 sides for a price of 204. Including the two regions full of type X plants, this map has a total price of 236.

This map has a total price of 368:

AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA

It includes two regions full of type B plants (each with 4 sides) and a single region full of type A plants (with 4 sides on the outside and 8 more sides on the inside, a total of 12 sides). Be especially careful when counting the fence around regions like the one full of type A plants; in particular, each section of fence has an in-side and an out-side, so the fence does not connect across the middle of the region (where the two B regions touch diagonally). (The Elves would have used the Möbius Fencing Company instead, but their contract terms were too one-sided.)

The larger example from before now has the following updated prices:

    A region of R plants with price 12 * 10 = 120.
    A region of I plants with price 4 * 4 = 16.
    A region of C plants with price 14 * 22 = 308.
    A region of F plants with price 10 * 12 = 120.
    A region of V plants with price 13 * 10 = 130.
    A region of J plants with price 11 * 12 = 132.
    A region of C plants with price 1 * 4 = 4.
    A region of E plants with price 13 * 8 = 104.
    A region of I plants with price 14 * 16 = 224.
    A region of M plants with price 5 * 6 = 30.
    A region of S plants with price 3 * 6 = 18.

Adding these together produces its new total price of 1206.

What is the new total price of fencing all regions on your map?

'''
from matrix import Matrix

def main():
    garden_map = GardenMap.from_inputfile('data/aoc24_input_12.txt')
#    garden_map = GardenMap.from_inputfile('data/test12.txt')
    print(garden_map.total_price())

class GardenMap(Matrix):
    def __init__(self, matrix):
        super().__init__(matrix)
        self.regions = self.get_regions()

    def get_regions(self):
        ## each region maps their top-left coordinate to the list of plots.
        regions = dict()
        for y in range(self.height):
            for x in range(self.width):
                is_in_region = False
                for region in regions.values():
                    if region.includes_plot(x, y, self.get(x, y)):
                        is_in_region = True
                        break
                if not is_in_region:
                    area = set()
                    search_stack = [(x, y)]
                    id = self.get(x, y)
                    while len(search_stack) > 0:
                        plot = search_stack.pop()
                        if plot not in area:
                            area.add(plot)
                            for neighbor in self.get_neighbors(plot[0], plot[1]):
                                if self.get(neighbor[0], neighbor[1]) == id:
                                    search_stack.append(neighbor)
                    regions[(x, y)] = Region(id, list(area))
        return regions
    
    def total_price(self):
        return sum([region.get_price() for region in self.regions.values()])

class Region():
    def __init__(self, identifier, plots:list):
        self.plots = plots
        self.identifier = identifier
        self.area = len(plots)
#        self.perimeter = self._calculate_perimeter()
        self.sides = self._calculate_sides()
    
    def _calculate_perimeter(self):
        perimeter = 0
        for plot in self.plots:
            plot_neighbors = [(plot[0] + x, plot[1] + y) for (x, y) in [(0,1), (1, 0), (0, -1), (-1, 0)]]
            for neighbor in plot_neighbors:
                if neighbor not in self.plots:
                    perimeter += 1
        return perimeter

    def _calculate_sides(self):
        ## map all lists of plots forming a side to their corresponding direction
        sides = dict()
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for direction in directions:
            sides[direction] = []
        for plot in self.plots:
            for direction in directions:
                # Make sure the plot and direction are not already included in another side definition
                if any(plot in side for side in sides[direction]):
                    continue
                if (plot[0] + direction[0], plot[1] + direction[1]) not in self.plots:
                    new_side = []
                    orthogonal_d = [(direction[1], direction[0]), (-direction[1], -direction[0])]
                    search_stack = [(plot, orthogonal_d)]
                    while len(search_stack) > 0:
                        p, dir = search_stack.pop()
                        new_side.append(p)
                        adjacent_pos = [((p[0] + d[0], p[1] + d[1]), d) for d in dir ]
                        for ap, d in adjacent_pos:
                            ## here we are looking at the same direction as the initial one to see if we still have a straight line
                            if ap in self.plots and (ap[0] + direction[0], ap[1] + direction[1]) not in self.plots:
                                search_stack.append((ap, [d]))
                    sides[direction].append(new_side)
        return sum(len(side) for side in sides.values())
                
    def includes_plot(self, x, y, identifier):
        return (x, y) in self.plots and self.identifier == identifier
    
    def get_price(self):
        return self.area * self.sides

if __name__ == '__main__':
    main()