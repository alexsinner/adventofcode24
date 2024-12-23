'''
--- Part Two ---

There are still way too many results to go through them all. You'll have to find the LAN party another way and go there yourself.

Since it doesn't seem like any employees are around, you figure they must all be at the LAN party. If that's true, the LAN party will be the largest set of computers that are all connected to each other. That is, for each computer at the LAN party, that computer will have a connection to every other computer at the LAN party.

In the above example, the largest set of computers that are all connected to each other is made up of co, de, ka, and ta. Each computer in this set has a connection to every other computer in the set:

ka-co
ta-co
de-co
ta-ka
de-ta
ka-de

The LAN party posters say that the password to get into the LAN party is the name of every computer at the LAN party, sorted alphabetically, then joined together with commas. (The people running the LAN party are clearly a bunch of nerds.) In this example, the password would be co,de,ka,ta.

What is the password to get into the LAN party?
'''


def main():
    inputfile = 'data/aoc24_input_23.txt'
    connections = parse_inputfile(inputfile)
    # it looks like each node is connected to 13 other nodes
    mutuals = find_interconnected_sets(connections)
    for m in mutuals:
        if len(m) > 12:
            print(','.join(m))

def find_interconnected_sets(connections):
    mutual_connections = set()
    for key, value in connections.items():
        connected = set()
        connected.add(key)
        for i in range(len(value)):
            # if value[i] is connected to each item in the set, it can be added
            if all(existing in connections[value[i]] for existing in connected):
                connected.add(value[i])
        connected = list(connected)
        connected.sort()
        mutual_connections.add(tuple(connected))
    return mutual_connections


def parse_inputfile(inputfile):
    connections = dict()
    with open(inputfile, 'r') as f:
        for line in f.readlines():
            connection = line.strip().split('-')
            if connection[0] in connections:
                connections[connection[0]].append(connection[1])
            else:
                connections[connection[0]] = [connection[1]]
            if connection[1] in connections:
                connections[connection[1]].append(connection[0])
            else:
                connections[connection[1]] = [connection[0]]
    return connections # a dict where each node is mapped to connected 




if __name__ == '__main__':
    main()