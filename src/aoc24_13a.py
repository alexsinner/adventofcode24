'''
--- Day 13: Claw Contraption ---

Next up: the lobby of a resort on a tropical island. The Historians take a moment to admire the hexagonal floor tiles before spreading out.

Fortunately, it looks like the resort has a new arcade! Maybe you can win some prizes from the claw machines?

The claw machines here are a little unusual. Instead of a joystick or directional buttons to control the claw, these machines have two buttons labeled A and B. Worse, you can't just put in a token and play; it costs 3 tokens to push the A button and 1 token to push the B button.

With a little experimentation, you figure out that each machine's buttons are configured to move the claw a specific amount to the right (along the X axis) and a specific amount forward (along the Y axis) each time that button is pressed.

Each machine contains one prize; to win the prize, the claw must be positioned exactly above the prize on both the X and Y axes.

You wonder: what is the smallest number of tokens you would have to spend to win as many prizes as possible? You assemble a list of every machine's button behavior and prize location (your puzzle input). For example:

Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279

This list describes the button configuration and prize location of four different claw machines.

For now, consider just the first claw machine in the list:

    Pushing the machine's A button would move the claw 94 units along the X axis and 34 units along the Y axis.
    Pushing the B button would move the claw 22 units along the X axis and 67 units along the Y axis.
    The prize is located at X=8400, Y=5400; this means that from the claw's initial position, it would need to move exactly 8400 units along the X axis and exactly 5400 units along the Y axis to be perfectly aligned with the prize in this machine.

The cheapest way to win the prize is by pushing the A button 80 times and the B button 40 times. This would line up the claw along the X axis (because 80*94 + 40*22 = 8400) and along the Y axis (because 80*34 + 40*67 = 5400). Doing this would cost 80*3 tokens for the A presses and 40*1 for the B presses, a total of 280 tokens.

For the second and fourth claw machines, there is no combination of A and B presses that will ever win a prize.

For the third claw machine, the cheapest way to win the prize is by pushing the A button 38 times and the B button 86 times. Doing this would cost a total of 200 tokens.

So, the most prizes you could possibly win is two; the minimum tokens you would have to spend to win all (two) prizes is 480.

You estimate that each button would need to be pressed no more than 100 times to win a prize. How else would someone be expected to play?

Figure out how to win as many prizes as possible. What is the fewest tokens you would have to spend to win all possible prizes?
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

    def solve(self, max_presses=100):
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
#        a_moves = (p_x*a_x*b_y)/((a_x**2)*b_y+(a_x*a_y*b_x)) - (p_y*b_x)/((a_x*b_y)+(a_y*b_x))
        a_moves = (p_x*b_y-p_y*b_x)/(a_x*b_y-a_y*b_x)
        b_moves = (p_y-(a_moves*a_y))/b_y
        if a_moves < 0 or b_moves < 0:
            return 0
        elif a_moves > max_presses or b_moves > max_presses:
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
                        prize = (int(match.group(1)), int(match.group(2)))
                    claw_machines.append(cls(button_a, button_b, prize))
                else:
                    continue    
            return claw_machines
        
if __name__ == "__main__":
    main()