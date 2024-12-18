'''
--- Day 17: Chronospatial Computer ---

The Historians push the button on their strange device, but this time, you all just feel like you're falling.

"Situation critical", the device announces in a familiar voice. "Bootstrapping process failed. Initializing debugger...."

The small handheld device suddenly unfolds into an entire computer! The Historians look around nervously before one of them tosses it to you.

This seems to be a 3-bit computer: its program is a list of 3-bit numbers (0 through 7), like 0,1,2,3. The computer also has three registers named A, B, and C, but these registers aren't limited to 3 bits and can instead hold any integer.

The computer knows eight instructions, each identified by a 3-bit number (called the instruction's opcode). Each instruction also reads the 3-bit number after it as an input; this is called its operand.

A number called the instruction pointer identifies the position in the program from which the next opcode will be read; it starts at 0, pointing at the first 3-bit number in the program. Except for jump instructions, the instruction pointer increases by 2 after each instruction is processed (to move past the instruction's opcode and its operand). If the computer tries to read an opcode past the end of the program, it instead halts.

So, the program 0,1,2,3 would run the instruction whose opcode is 0 and pass it the operand 1, then run the instruction having opcode 2 and pass it the operand 3, then halt.

There are two types of operands; each instruction specifies the type of its operand. The value of a literal operand is the operand itself. For example, the value of the literal operand 7 is the number 7. The value of a combo operand can be found as follows:

    Combo operands 0 through 3 represent literal values 0 through 3.
    Combo operand 4 represents the value of register A.
    Combo operand 5 represents the value of register B.
    Combo operand 6 represents the value of register C.
    Combo operand 7 is reserved and will not appear in valid programs.

The eight instructions are as follows:

The adv instruction (opcode 0) performs division. The numerator is the value in the A register. The denominator is found by raising 2 to the power of the instruction's combo operand. (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.) The result of the division operation is truncated to an integer and then written to the A register.

The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal operand, then stores the result in register B.

The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 (thereby keeping only its lowest 3 bits), then writes that value to the B register.

The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register is not zero, it jumps by setting the instruction pointer to the value of its literal operand; if this instruction jumps, the instruction pointer is not increased by 2 after this instruction.

The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C, then stores the result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)

The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value. (If a program outputs multiple values, they are separated by commas.)

The bdv instruction (opcode 6) works exactly like the adv instruction except that the result is stored in the B register. (The numerator is still read from the A register.)

The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is stored in the C register. (The numerator is still read from the A register.)

Here are some examples of instruction operation:

    If register C contains 9, the program 2,6 would set register B to 1.
    If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2.
    If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A.
    If register B contains 29, the program 1,7 would set register B to 26.
    If register B contains 2024 and register C contains 43690, the program 4,0 would set register B to 44354.

The Historians' strange device has finished initializing its debugger and is displaying some information about the program it is trying to run (your puzzle input). For example:

Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0

Your first task is to determine what the program is trying to output. To do this, initialize the registers to the given values, then run the given program, collecting any output produced by out instructions. (Always join the values produced by out instructions with commas.) After the above program halts, its final output will be 4,6,3,5,6,3,5,2,1,0.

Using the information provided by the debugger, initialize the registers to the given values, then run the program. Once it halts, what do you get if you use commas to join the values it output into a single string?
'''

def main():
    inputfile = 'data/aoc24_input_17.txt'
    computer = Computer.from_inputfile(inputfile)
    computer.run()
    print(','.join([str(x) for x in computer.output]))

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


if __name__ == '__main__':
    main()
