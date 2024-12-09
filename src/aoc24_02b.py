'''
--- Part Two ---

The engineers are surprised by the low number of safe reports until they realize they forgot to tell you about the Problem Dampener.

The Problem Dampener is a reactor-mounted module that lets the reactor safety systems tolerate a single bad level in what would otherwise be a safe report. It's like the bad level never happened!

Now, the same rules apply as before, except if removing a single level from an unsafe report would make it safe, the report instead counts as safe.

More of the above example's reports are now safe:

    7 6 4 2 1: Safe without removing any level.
    1 2 7 8 9: Unsafe regardless of which level is removed.
    9 7 6 2 1: Unsafe regardless of which level is removed.
    1 3 2 4 5: Safe by removing the second level, 3.
    8 6 4 4 1: Safe by removing the third level, 4.
    1 3 6 7 9: Safe without removing any level.

Thanks to the Problem Dampener, 4 reports are actually safe!

Update your analysis by handling situations where the Problem Dampener can remove a single level from unsafe reports. How many reports are now safe?
'''

def main():
    input_file = './data/aoc24_input_02.txt'
    safe_count = 0
    for l in parse_input(input_file):
        safe = is_safe_with_dampener(l)
        if safe:
            safe_count += 1
        else:
            print(str(l))

    print(safe_count)

# check for the following unsafe scenarios:
# 1. maximum difference of increase/decreas > 3
# 2. list includes both increases and decreases
def is_safe(l):
    deltas = [l[i+1] - l[i] for i in range(len(l)-1)]
    if max(deltas) > 3 or min(deltas) < -3:
        return False
    if max(deltas) > 0 and min(deltas) < 0:
        return False
    if 0 in deltas:
        return False
    return True

# check for the following unsafe scenarios:
# 1. maximum difference of increase/decreas > 3
# 2. list includes both increases and decreases
def is_safe_with_dampener(l):
    max_level = 0
    min_level = 0
    for i in range(len(l)-1):
        delta = l[i+1] - l[i]
        max_level = max(delta, max_level)
        min_level = min(delta, min_level)
        if delta > 3 or delta < -3 or delta == 0 or (max_level > 0 and min_level < 0):
            ## Need to test the different scenarios that could have led to breaking
            ## easy to miss scenario: up down down or down up up -> need to remove the first index
            ## we need to remove the broken element
            new_list1 = l[:i+1] + l[i+2:]
#            print("new list 1: " + str(new_list1)+ " removed index " + str(i+1))
            new_list2 = l[:i] + l[i+1:]
#            print("new list 2: " + str(new_list2)+ " removed index " + str(i))
            new_list3 = l[1:]
            return is_safe(new_list1) or is_safe(new_list2) or is_safe(new_list3)
    return True

'''
def is_safe_with_dampener2(l):
    deltas = [l[i+1] - l[i] for i in range(len(l)-1)]
    max_d = 0
    min_d = 0
    for i in range(len(deltas)):
        max_d = max(deltas[i], max_d)
        min_d = min(deltas[i], min_d)
        if deltas[i] > 3 or deltas[i] < -3 or deltas[i] == 0 or (max_d > 0 and min_d < 0):


            new_list = l[:i] + l[i+1:]
            return is_safe(new_list)

    for i in range(len(l)-1):
        new_list = l[:i] + l[i+1:]
        if is_safe(new_list):
            return True
    return False
'''
    # Read an input file of space-separated numbers. Each line represent a list of numbers.
# @return: a list of lists of numbers
def parse_input(input_file):
    return_list = []
    with open(input_file) as f:
        for line in f.readlines():
            return_list.append([int(x) for x in line.split(" ")])
    return return_list


if __name__ == '__main__':
    main()