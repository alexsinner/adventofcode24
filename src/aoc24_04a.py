'''--- Day 4: Ceres Search ---

"Looks like the Chief's not here. Next!" One of The Historians pulls out a device and pushes the only button on it. After a brief flash, you recognize the interior of the Ceres monitoring station!

As the search for the Chief continues, a small Elf who lives on the station tugs on your shirt; she'd like to know if you could help her with her word search (your puzzle input). She only has to find one word: XMAS.

This word search allows words to be horizontal, vertical, diagonal, written backwards, or even overlapping other words. It's a little unusual, though, as you don't merely need to find one instance of XMAS - you need to find all of them. Here are a few ways XMAS might appear, where irrelevant characters have been replaced with .:

..X...
.SAMX.
.A..A.
XMAS.S
.X....

The actual word search will be full of letters instead. For example:

MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX

In this word search, XMAS occurs a total of 18 times; here's the same word search again, but where letters not involved in any XMAS have been replaced with .:

....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX

Take a look at the little Elf's word search. How many times does XMAS appear?
'''
import re
from matrix import Matrix

def main():
    '''Main function to read input, process data, and print the result.'''
    input_file = "data/aoc24_input_04.txt"
#    input_file = "data/test04.txt"
    input = Matrix.from_inputfile(input_file)
    total = 0
    print([''.join(x) for x in input.matrix])
    for row in matrix_to_strings(input):
        print(row + " " +str(count_xmas(row)))
        total += count_xmas(row)
    print(total)

def count_xmas(input_string):
    matchcount = 0
    matchcount += len(re.findall(r'(XMAS)', input_string))
    matchcount += len(re.findall(r'(SAMX)', input_string))
    return matchcount

def matrix_to_strings(input_matrix):
    return_list = []
    # all horizontal rows as strings
    return_list.extend([''.join(x) for x in input_matrix.matrix])
    # all vertical columns as strings
    return_list.extend([''.join(x) for x in zip(*input_matrix.matrix)])
    # all diagonals as strings
    return_list.extend(get_diagonals(input_matrix))
    return (return_list)


def get_diagonals(input_matrix):
    diagonals = []
    # first get all the diagonals from the top row
    for x in range(len(input_matrix.matrix[0])):
        new_row = ''
        posx, posy = (x, 0) 
        while not input_matrix.is_out_of_bounds((posx, posy)):
            new_row += input_matrix.get(posx, posy)
            posx +=1
            posy +=1
        diagonals.append(new_row)
    # then all the diagonals from the left column
    for y in range(1, len(input_matrix.matrix)):
        new_row = ''
        posx, posy = (0, y)
        while not input_matrix.is_out_of_bounds((posx, posy)):
            new_row += input_matrix.get(posx, posy)
            posx +=1
            posy +=1
        diagonals.append(new_row)
    # now we start with the top row, but right to left
    for x in range(len(input_matrix.matrix[0])-1, -1, -1):
        new_row = ''
        posx, posy = (x, 0)
        while not input_matrix.is_out_of_bounds((posx, posy)):
            new_row += input_matrix.get(posx, posy)
            posx -=1
            posy +=1
        diagonals.append(new_row)
    # finally diagonals from the right column 
    for y in range(1, len(input_matrix.matrix)):
        new_row = ''
        posx, posy = (len(input_matrix.matrix[0])-1, y)
        while not input_matrix.is_out_of_bounds((posx, posy)):
            new_row += input_matrix.get(posx, posy)
            posx -=1
            posy +=1
        diagonals.append(new_row)
    return diagonals


if __name__ == '__main__':
    main()