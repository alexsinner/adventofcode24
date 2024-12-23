'''
--- Part Two ---

Digging deeper in the device's manual, you discover the problem: this program is supposed to output another copy of the program! Unfortunately, the value in register A seems to have been corrupted. You'll need to find a new value to which you can initialize register A so that the program's output instructions produce an exact copy of the program itself.

For example:

Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0

This program outputs a copy of itself if register A is instead initialized to 117440. (The original initial value of register A, 2024, is ignored.)

What is the lowest positive initial value for register A that causes the program to output a copy of itself?

Program is:
    b = a%8
    b = b xor 2
    c = int(a / 2**b)
    b = b xor 7
    b = b xor c
    a = int(a / 2**3)
    out b%8
    if a!=0 jmp 0
'''


def main():
    inputfile = 'data/aoc24_input_17.txt'
    computer = Computer.from_inputfile(inputfile)
    program = computer.program
    print(f'A: {find_a(program)}')

def find_a(program):
    '''
    Iterate over values of a, starting from zero. once the last program element is matched, multiply by 8, then continue until the last 2 are matched, multiply by 8, etc until the program is matched
    '''
    a = 0
    while True:
        computer = Computer(program, a, 0, 0)
        computer.run()
        if computer.output == program:
            return a
        if computer.output == program[-len(computer.output):]:
            a = a * 8
        else:
            a += 1        


class Computer():

    def __init__(self, program, a=0, b=0, c=0):
        self.program = program
        self.a = a
        self.b = b
        self.c = c
        self.ip = 0
        self.output = []

    @classmethod
    def from_inputfile(cls, inputfile):
        a, b, c = 0, 0, 0
        program = []
        with open(inputfile) as f:
            for line in f.readlines():
                if line.startswith('Register A:'):
                    a = int(line.split(':')[1])
                elif line.startswith('Register B:'):
                    b = int(line.split(':')[1])
                elif line.startswith('Register C:'):
                    c = int(line.split(':')[1])
                elif line.startswith('Program:'):
                    program.extend([int(x) for x in line.split(':')[1].split(',')])
                else:
                    continue
        return cls(program, a, b, c)

    def get_combo_operand(self, operand):
        if operand < 4:
            return operand
        elif operand == 4:
            return self.a
        elif operand == 5:
            return self.b
        elif operand == 6:
            return self.c
        else:
            return 0

    def run(self):
        while self.ip < len(self.program):
            opcode = self.program[self.ip] % 8
            operand = self.program[self.ip + 1]
            self.execute(opcode, operand)
            self.ip += 2

    def execute(self, opcode, operand):
        if opcode == 0:
            return self.adv(operand)
        elif opcode == 1:
            return self.bxl(operand)
        elif opcode == 2:
            return self.bst(operand)
        elif opcode == 3:
            return self.jnz(operand)
        elif opcode == 4:
            return self.bxc(operand)
        elif opcode == 5:
            return self.out(operand)
        elif opcode == 6:
            return self.bdv(operand)
        elif opcode == 7:
            return self.cdv(operand)
        else:
            raise ValueError('Unknown opcode: ' + str(opcode))

    def adv(self, operand):
        '''The adv instruction (opcode 0) performs division. The numerator is the value in the A register. The denominator is found by raising 2 to the power of the instruction's combo operand. (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.) The result of the division operation is truncated to an integer and then written to the A register.'''
        self.a = int(self.a / (2 ** self.get_combo_operand(operand)))
        return self.a

    def bxl(self, operand):
        '''The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal operand, then stores the result in register B.'''
        self.b ^= operand
        return self.b
    
    def bst(self, operand):
        '''The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 (thereby keeping only its lowest 3 bits), then writes that value to the B register.'''
        self.b = self.get_combo_operand(operand) % 8
        return self.b
    
    def jnz(self, operand):
        '''The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register is not zero, it jumps by setting the instruction pointer to the value of its literal operand; if this instruction jumps, the instruction pointer is not increased by 2 after this instruction.'''
        if self.a != 0:
            self.ip = operand - 2 ## TBC if this is the correct approach

    def bxc(self, operand):
        '''The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C, then stores the result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)'''
        self.b ^= self.c
        return self.b

    def out(self, operand):
        '''The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value. (If a program outputs multiple values, they are separated by commas.)'''
        self.output.append(self.get_combo_operand(operand) % 8)
        return self.get_combo_operand(operand) % 8
    
    def bdv(self, operand):
        '''The bdv instruction (opcode 6) works exactly like the adv instruction except that the result is stored in the B register. (The numerator is still read from the A register.)'''
        self.b = int(self.a / (2 ** self.get_combo_operand(operand)))
        return self.b

    def cdv(self, operand):
        '''The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is stored in the C register. (The numerator is still read from the A register.)'''
        self.c = int(self.a / (2 ** self.get_combo_operand(operand)))
        return self.c

    def __str__(self):
        return 'A: ' + str(self.a) + ' B: ' + str(self.b) + ' C: ' + str(self.c) + ' IP: ' + str(self.ip)

if __name__ == '__main__':
    main()
