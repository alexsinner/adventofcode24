'''
--- Day 19: Linen Layout ---

--- Part Two ---

The staff don't really like some of the towel arrangements you came up with. To avoid an endless cycle of towel rearrangement, maybe you should just give them every possible option.

Here are all of the different ways the above example's designs can be made:

brwrr can be made in two different ways: b, r, wr, r or br, wr, r.

bggr can only be made with b, g, g, and r.

gbbr can be made 4 different ways:

    g, b, b, r
    g, b, br
    gb, b, r
    gb, br

rrbgbr can be made 6 different ways:

    r, r, b, g, b, r
    r, r, b, g, br
    r, r, b, gb, r
    r, rb, g, b, r
    r, rb, g, br
    r, rb, gb, r

bwurrg can only be made with bwu, r, r, and g.

brgr can be made in two different ways: b, r, g, r or br, g, r.

ubwu and bbrgwb are still impossible.

Adding up all of the ways the towels in this example could be arranged into the desired designs yields 16 (2 + 1 + 4 + 6 + 1 + 2).

They'll let you into the onsen as soon as you have the list. What do you get if you add up the number of different ways you could make each design?

'''
memory = dict()

def main():
    inputfile='data/aoc24_input_19.txt'
    patterns, designs = parse_input_file(inputfile)
    total_possible = 0
    for design in designs:
        possible_designs = get_possible_designs(patterns, design)
        print(f'{design}: {possible_designs}')
        total_possible += possible_designs
    print(f'Total possible designs: {total_possible}')

def is_possible(patterns, design):
    visited = set()
    start_node = ('', design)
    queue = [start_node]
    while len(queue) > 0:
        node = queue.pop(0)
        if node[0] == design:
            return True
        else:
            for pattern in patterns:
                if node[1].startswith(pattern):
                    new_node = (node[0] + pattern, node[1][len(pattern):])
                    if new_node in visited:
                        continue
                    else:
                        visited.add(new_node)
                        queue.append(new_node)
    return False

def get_possible_designs(patterns, design):
    if design in memory:
        return memory[design]
    elif not is_possible(patterns, design):
        memory[design] = 0
        return 0
    possible_designs = 0
    for pattern in patterns:
        if pattern == design:
            possible_designs += 1
        elif design.startswith(pattern):
            possible_designs += get_possible_designs(patterns, design[len(pattern):])
        else:
            continue
    memory[design] = possible_designs
    return possible_designs

def parse_input_file(inputfile):
    patterns = []
    designs = []
    with open(inputfile) as f:
        for line in f:
            line = line.strip()
            if line == '':
                continue
            if line.find(',') != -1:
                patterns = [p.strip() for p in line.split(',')]
            else:
                designs.append(line)
    return patterns, designs

if __name__ == '__main__':
    main()