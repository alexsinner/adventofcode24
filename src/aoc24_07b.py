'''
--- Part Two ---

The engineers seem concerned; the total calibration result you gave them is nowhere close to being within safety tolerances. Just then, you spot your mistake: some well-hidden elephants are holding a third type of operator.

The concatenation operator (||) combines the digits from its left and right inputs into a single number. For example, 12 || 345 would become 12345. All operators are still evaluated left-to-right.

Now, apart from the three equations that could be made true using only addition and multiplication, the above example has three more equations that can be made true by inserting operators:

    156: 15 6 can be made true through a single concatenation: 15 || 6 = 156.
    7290: 6 8 6 15 can be made true using 6 * 8 || 6 * 15.
    192: 17 8 14 can be made true using 17 || 8 + 14.

Adding up all six test values (the three that could be made before using only + and * plus the new three that can now be made by also using ||) produces the new total calibration result of 11387.

Using your new knowledge of elephant hiding spots, determine which equations could possibly be true. What is their total calibration result?
'''


def main():
    inputfile = "data/aoc24_input_07.txt"
    total = 0
    with open(inputfile) as f:
        lines = f.readlines()
        for line in lines:
            equation = Equation(line)
            if equation.solve():
                total += equation.result
#            break
    print(total)

class Equation:
    operators = ('+', '*', '||')
    def __init__(self, line):
        self.line = line
        self.result = int(line.strip().split(':')[0])
        right = line.strip().split(':')[1]
        self.operands = [int(x) for x in right.strip().split(' ')]

    def operate(self, value, operator, operand):
        returnvalue = value
        if operator == '+':
            returnvalue += operand
        elif operator == '*':
            returnvalue *= operand
        elif operator == '||':
            returnvalue = int(str(value) + str(operand))
        else:
            returnvalue = operand
        print(str(value) + operator + str(operand) + '=' + str(returnvalue))
        return returnvalue

    def solve(self):
        value = self.operands[0]
        dfs_stack = []
        depth = 0
        dfs_stack.append((value, '', self.operands[0], depth))
        max_depth = len(self.operands) -1
        while len(dfs_stack) > 0:
            value, operator, operand, depth = dfs_stack.pop()
            value = self.operate(value, operator, operand)
            if depth < max_depth:
                depth += 1
                for i in range(len(self.operators)):
                    dfs_stack.append((value, self.operators[i],self.operands[depth], depth))
            else:
                if value == self.result and depth == max_depth:
                    return True
                
    def __str__(self):
        return self.line.strip()
    
if __name__ == '__main__':
    main()