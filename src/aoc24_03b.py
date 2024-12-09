'''
--- Part Two ---

As you scan through the corrupted memory, you notice that some of the conditional statements are also still intact. If you handle some of the uncorrupted conditional statements in the program, you might be able to get an even more accurate result.

There are two new instructions you'll need to handle:

    The do() instruction enables future mul instructions.
    The don't() instruction disables future mul instructions.

Only the most recent do() or don't() instruction applies. At the beginning of the program, mul instructions are enabled.

For example:

xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))

This corrupted memory is similar to the example from before, but this time the mul(5,5) and mul(11,8) instructions are disabled because there is a don't() instruction before them. The other mul instructions function normally, including the one at the end that gets re-enabled by a do() instruction.

This time, the sum of the results is 48 (2*4 + 8*5).

Handle the new instructions; what do you get if you add up all of the results of just the enabled multiplications?

'''
import re

def main():
    input_file = "data/aoc24_input_03.txt"
    multiplications = parse_input(input_file)
    total = 0
    for (a, b) in multiplications:
        total += a*b
    print(total)

def parse_input(input_file):
    '''reads the input file and returns a list of tuples to be multiplied'''
    with open(input_file) as f:
        ## pattern identifying all parts between do() and don't(), including newlines
        ## pattern also needs to include start of string until dont() and d() until end of string
        dodont_pattern = re.compile(r'(do\(\)(.*)don\'t\(\))', re.DOTALL)
        ## pattern to identify all mul() patterns
        valid_mul_pattern = re.compile(r'mul\((\d+),(\d+)\)')
        return_list = []
        instruction_string = f.read()
        i = 0
        mul_enabled = True
        enabled_instruction_string = ''
        ## identify all the locations of do and don't in the string
        while i >= 0:
            if mul_enabled:
                start = i
                end = instruction_string.find("don't()", start)
                enabled_instruction_string += instruction_string[i:end]
                i = end
                mul_enabled = False
            else:
                i = instruction_string.find("do()", i)
                mul_enabled = True
        matches = valid_mul_pattern.findall(enabled_instruction_string)
        for match in matches:
            return_list.append((int(match[0]), int(match[1])))
        return return_list

if __name__ == '__main__':
    main()