'''
--- Part Two ---

Upon completion, two things immediately become clear. First, the disk definitely has a lot more contiguous free space, just like the amphipod hoped. Second, the computer is running much more slowly! Maybe introducing all of that file system fragmentation was a bad idea?

The eager amphipod already has a new plan: rather than move individual blocks, he'd like to try compacting the files on his disk by moving whole files instead.

This time, attempt to move whole files to the leftmost span of free space blocks that could fit the file. Attempt to move each file exactly once in order of decreasing file ID number starting with the file with the highest file ID number. If there is no span of free space to the left of a file that is large enough to fit the file, the file does not move.

The first example from above now proceeds differently:

00...111...2...333.44.5555.6666.777.888899
0099.111...2...333.44.5555.6666.777.8888..
0099.1117772...333.44.5555.6666.....8888..
0099.111777244.333....5555.6666.....8888..
00992111777.44.333....5555.6666.....8888..

The process of updating the filesystem checksum is the same; now, this example's checksum would be 2858.

Start over, now compacting the amphipod's hard drive using this new method instead. What is the resulting filesystem checksum?
'''

def main():
    inputfile = "data/aoc24_input_09.txt"
#    diskmap = '2333133121414131402'
    diskmap = read_inputfile(inputfile)
    comp = Compressor(diskmap)
    print(comp)
    print(comp.checksum())

def read_inputfile(inputfile):
    with open(inputfile) as f:
        return f.read().strip() 

class Compressor:
    def __init__(self, inputline):
        self.diskmap = inputline
        # this is an array of numbers and None values representing empty space
        self.blocks = self.decompress()
        self.blocks = self.compress()

    def decompress(self):
        # now the block-array is a list of tuples (fileid, size)
        block_array = []
        ## if the length is not even, add 0 empty spaces to the end
        if len(self.diskmap) % 2 != 0:
            self.diskmap += '0'
        decompressed = zip(self.diskmap[::2], self.diskmap[1::2])
        for i, value in enumerate(decompressed):
            block_array.append((i, int(value[0])))
            block_array.append((None,int(value[1])))
        return block_array

    def compress(self):
        # find the next empty space
        for i in range(len(self.blocks)):
            if self.blocks[i][0] == None:
                available_space = self.blocks[i][1]
                for j in range(len(self.blocks) - 1, i, -1):
                    if self.blocks[j][0] != None and self.blocks[j][1] <= available_space:
                        self.blocks[i] = self.blocks[j]
                        self.blocks[j] = (None, self.blocks[j][1])
                        if available_space > self.blocks[j][1]:
                            self.blocks.insert(i+1, (None, available_space - self.blocks[j][1]))
                        break
        ## TBD: do I have to consolidate empty spaces?
        return self.blocks

    def checksum(self):
        expanded_blocks = []
        for block in self.blocks:
            expanded_blocks.extend([block[0]]*block[1])
        print(expanded_blocks)
        return sum([i * block for i, block in enumerate(expanded_blocks) if block != None])

    def __str__(self):
        return f'{self.diskmap}' + '--->' + f'{self.blocks}'

if __name__ == '__main__':
    main()