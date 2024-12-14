'''
--- Part Two ---

As you go to win the first prize, you discover that the claw is nowhere near where you expected it would be. Due to a unit conversion error in your measurements, the position of every prize is actually 10000000000000 higher on both the X and Y axis!

Add 10000000000000 to the X and Y position of every prize. After making this change, the example above would now look like this:

Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=10000000008400, Y=10000000005400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=10000000012748, Y=10000000012176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=10000000007870, Y=10000000006450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=10000000018641, Y=10000000010279

Now, it is only possible to win a prize on the second and fourth claw machines. Unfortunately, it will take many more than 100 presses to do so.

Using the corrected prize coordinates, figure out how to win as many prizes as possible. What is the fewest tokens you would have to spend to win all possible prizes?

'''
import re
from priorityqueue import PriorityQueue

def main():
    claw_machines = ClawMachine.from_input_file("data/aoc24_input_13.txt")
    total = 0
    for c in claw_machines:
        total += c.solve()
    print(total)

class ClawMachine:
    def __init__(self, button_a, button_b, prize, cost_a = 3, cost_b = 1):
        self.button_a = button_a
        self.button_b = button_b
        self.prize = prize
        self.cost_a = cost_a
        self.cost_b = cost_b

    def solve(self):
        ''' finds the lowest cost to reach the prize and returns it'''
        # solving the equation system
        # p_x = a_moves * a_x + b_moves * b_x
        # p_y = a_moves * a_y + b_moves * b_y
        p_x = self.prize[0]
        p_y = self.prize[1]
        a_x = self.button_a[0]
        a_y = self.button_a[1]
        b_x = self.button_b[0]
        b_y = self.button_b[1]
        a_moves = (p_x*b_y-p_y*b_x)/(a_x*b_y-a_y*b_x)
        b_moves = (p_y-(a_moves*a_y))/b_y
        if a_moves < 0 or b_moves < 0:
            return 0
        elif not a_moves.is_integer() or not b_moves.is_integer():
            return 0
        else:
            return int(a_moves*self.cost_a + b_moves*self.cost_b)

    def __str__(self):
        return f"Button A: {self.button_a}, Button B: {self.button_b}, Prize: {self.prize}"
    
    @classmethod
    def from_input_file(cls, input_file):
        ''' parses an inputfile where each ClawMachine is specified with 3 lines. Definitions are separated by an empty line.
        Example:
        Button A: X+16, Y+32
        Button B: X+53, Y+11
        Prize: X=6788, Y=4716
        '''
        with open(input_file, 'r') as f:
            lines = f.readlines()
            claw_machines = []
            button_pattern = re.compile(r'X\+(\d+), Y\+(\d+)')
            prize_pattern = re.compile(r'X=(\d+), Y=(\d+)')
            button_a = None
            button_b = None
            prize = None
            for line in lines:
                if line.startswith("Button A"):
                    match = button_pattern.search(line)
                    if match:
                        button_a = (int(match.group(1)), int(match.group(2)))
                elif line.startswith("Button B"):
                    match = button_pattern.search(line)
                    if match:
                        button_b = (int(match.group(1)), int(match.group(2)))
                elif line.startswith("Prize"):
                    match = prize_pattern.search(line)
                    if match:
                        prize = (int(match.group(1))+10000000000000, int(match.group(2))+10000000000000)
                    claw_machines.append(cls(button_a, button_b, prize))
                else:
                    continue    
            return claw_machines
        
if __name__ == "__main__":
    main()