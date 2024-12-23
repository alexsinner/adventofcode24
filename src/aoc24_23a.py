'''--- Day 23: LAN Party ---

As The Historians wander around a secure area at Easter Bunny HQ, you come across posters for a LAN party scheduled for today! Maybe you can find it; you connect to a nearby datalink port and download a map of the local network (your puzzle input).

The network map provides a list of every connection between two computers. For example:

kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn

Each line of text in the network map represents a single connection; the line kh-tc represents a connection between the computer named kh and the computer named tc. Connections aren't directional; tc-kh would mean exactly the same thing.

LAN parties typically involve multiplayer games, so maybe you can locate it by finding groups of connected computers. Start by looking for sets of three computers where each computer in the set is connected to the other two computers.

In this example, there are 12 such sets of three inter-connected computers:

aq,cg,yn
aq,vc,wq
co,de,ka
co,de,ta
co,ka,ta
de,ka,ta
kh,qp,ub
qp,td,wh
tb,vc,wq
tc,td,wh
td,wh,yn
ub,vc,wq

If the Chief Historian is here, and he's at the LAN party, it would be best to know that right away. You're pretty sure his computer's name starts with t, so consider only sets of three computers where at least one computer's name starts with t. That narrows the list down to 7 sets of three inter-connected computers:

co,de,ta
co,ka,ta
de,ka,ta
qp,td,wh
tb,vc,wq
tc,td,wh
td,wh,yn

Find all the sets of three inter-connected computers. How many contain at least one computer with a name that starts with t?
'''

def main():
    inputfile = 'data/aoc24_input_23.txt'
    connections = parse_inputfile(inputfile)
    # it looks like each node is connected to 13 other nodes
    # for key, value in connections.items():
    #     print(key, value)
    mutuals = find_interconnected_sets(connections)
    total = 0
    for m in mutuals:
        if m[0].startswith('t') or m[1].startswith('t') or m[2].startswith('t'):
            total += 1
    print(f'Total sets of 3 connected computers where at least one starts with t: {total}')

def find_interconnected_sets(connections):
    mutual_connections = set()
    for key, value in connections.items():
        for i in range(len(value)-1):
            for j in range(i+1, len(value)):
                if key in connections[value[i]] and key in connections[value[j]] and value[i] in connections[value[j]]:
                    mutuals = [key]
                    mutuals.append(value[i])
                    mutuals.append(value[j])
                    mutuals.sort()
                    mutual_connections.add(tuple(mutuals))
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