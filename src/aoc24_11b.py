'''
--- Part Two ---

The Historians sure are taking a long time. To be fair, the infinite corridors are very large.

How many stones would you have after blinking a total of 75 times?
'''
import time

class StoneBag():

    def __init__(self, numbers):
        self.bag = dict()
        for number in numbers:
            self.add(number, 1)
        
    def add(self, number, times=1):
        if number in self.bag:
            self.bag[number] += times
        else:
            self.bag[number] = times

    def remove(self, number, times):
        if number in self.bag:
            self.bag[number] -= times
        else:
            self.bag[number] = 0


    def count(self):
        return sum(self.bag.values())
    
    @classmethod
    def from_inputfile(cls, inputfile):
        '''reads an inputfile and returns an instance of StoneBAg with all the numbers'''
        with open(inputfile) as f:
            input = f.read().strip()
            return cls([int(x) for x in input.split(' ')])
        
    def blink(self):
        '''applies the blink rules to each stone in the bag'''
        stones = [(s, self.bag[s]) for s in self.bag.keys() if self.bag[s]>0]
        for stone, times in stones:
            self.remove(stone, times)
            if stone == 0:
                self.add(1, times)
            elif len(str(stone)) % 2 == 0:
                left_part = int(str(stone)[:len(str(stone)) // 2])
                right_part = int(str(stone)[len(str(stone)) // 2:])
                self.add(left_part, times)
                self.add(right_part, times)
  #              print (f"{stone} to {left_part} and {right_part}")
            else:
                self.add(stone * 2024, times)
   #             print (f"{stone} to {stone * 2024}")
            
    def __str__(self):
        return str(self.number)
    
def main():
    inputfile = 'data/aoc24_input_11.txt'
    stones = StoneBag.from_inputfile(inputfile)
    start_time = time.perf_counter()
    for _ in range(75):
        stones.blink()
        print(f"{_+1} Number of stones: {stones.count()}")
    end_time = time.perf_counter()
    print(f"Execution time: {end_time - start_time:.6f} seconds")

if __name__ == '__main__':
    main()