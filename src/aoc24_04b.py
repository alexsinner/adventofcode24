'''
--- Part Two ---

The Elf looks quizzically at you. Did you misunderstand the assignment?

Looking for the instructions, you flip over the word search to find that this isn't actually an XMAS puzzle; it's an X-MAS puzzle in which you're supposed to find two MAS in the shape of an X. One way to achieve that is like this:

M.S
.A.
M.S

Irrelevant characters have again been replaced with . in the above diagram. Within the X, each MAS can be written forwards or backwards.

Here's the same example from before, but this time all of the X-MASes have been kept instead:

.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........

In this example, an X-MAS appears 9 times.

Flip the word search from the instructions back over to the word search side and try again. How many times does an X-MAS appear?
'''

import re
from matrix import Matrix

def main():
    '''Main function to read input, process data, and print the result.'''
    input_file = "data/aoc24_input_04.txt"
#    input_file = "data/test04.txt"
    input = Matrix.from_inputfile(input_file)
    total = 0
    for minime in iterate_3x3(input):
        if is_xmas(''.join(minime[::2])):
            total += 1
    print(total)

def iterate_3x3(input_matrix):
    for y in range(len(input_matrix.matrix)-2):
        for x in range(len(input_matrix.matrix[0])-2):
            yield [input_matrix.get(x+i, y+j) for j in range(3) for i in range(3)]


def is_xmas(input_string):
    return input_string in ['MSAMS', 'MMASS', 'SMASM', 'SSAMM']

if __name__ == '__main__':
    main()