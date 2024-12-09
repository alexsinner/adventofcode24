'''
--- Part Two ---

While the Elves get to work printing the correctly-ordered updates, you have a little time to fix the rest of them.

For each of the incorrectly-ordered updates, use the page ordering rules to put the page numbers in the after order. For the above example, here are the three incorrectly-ordered updates and their correct orderings:

    75,97,47,61,53 becomes 97,75,47,61,53.
    61,13,29 becomes 61,29,13.
    97,13,75,29,47 becomes 97,75,47,29,13.

After taking only the incorrectly-ordered updates and ordering them correctly, their middle page numbers are 47, 29, and 47. Adding these together produces 123.

Find the updates which are not in the correct order. What do you get if you add up the middle page numbers after correctly ordering just those updates?

'''

def main():
    inputfile = "data/aoc24_input_05.txt"
    (before_rules, after_rules, updates) = parse_input(inputfile)
    total = 0
    for update in updates:
        if (validate_update(before_rules, after_rules, update)) == 0:
            print("Invalid update:\n")
            print(update)
            for u in update:
                print(str(u) + " before " + str(before_rules[u]))
                print(str(u) + " after " + str(after_rules[u]))
            total += correct_update(before_rules, after_rules, update)
    print(total)
    

def correct_update(before_rules, after_rules, update):
    '''returns the correct ordering of the update list.'''
    # Approach to solve: for each element in the update list, split the list into before part and after part, and make sure that all elements of before part are in the after_rules dict entry for the element in question, and all elements in the after part are in the before_rules dict entry
    print(update)
    corrected_update = []
    ## iterate over the entire update list to put them into the correct place 
    # where every item in corrected_update before its position is in the after list of its dict entry, 
    # and everything afterr it is in the before rules of its entry
    for i in range(0, len(update)):
        element = update[i]
        if all(x in after_rules[element] for x in corrected_update):
            corrected_update.append(element)
        elif all(x in before_rules[element] for x in corrected_update):
            corrected_update.insert(0, element)
        else:
            for j in range(len(corrected_update)):
                before = corrected_update[:j]
                after = corrected_update[j:]
                if all(x in after_rules[update[i]] for x in before) and all(x in before_rules[update[i]] for x in after):
                    corrected_update.insert(j, update[i])
                    break
    validation = validate_update(before_rules, after_rules, corrected_update)
    if validation == 0:
        print("Error - update not valid")
    return validation


def validate_update(before_rules, after_rules, update):
    '''returns the middle element of the update list if the update is valid, otherwise return 0.
    An update is valid if all the rules are being followed.'''
    # Approach to solve: for each element in the update list, split the list into before part and after part, and make sure that all elements of before part are in the after_rules dict entry for the element in question, and all elements in the after part are in the before_rules dict entry
    for i in range(len(update)):
        before = update[:i]
        after = update[i+1:]
        if update[i] in after_rules:
            if not all(x in after_rules[update[i]] for x in before):
                return 0
        else:
            print("Error - element not in before rules")
        if update[i] in before_rules:
            if not all(x in before_rules[update[i]] for x in after):
                return 0
        else:
            print("Error - element not in before rules")
    return update[len(update)//2]

def parse_input(inputfile):
    before_rules = dict()
    after_rules = dict()
    updates = []
    with open(inputfile) as f:
        for line in f.readlines():
            if line.find('|') > 0:
                rule = line.split('|')
                if int(rule[0]) in before_rules:
                    before_rules[int(rule[0])].append(int(rule[1].strip()))
                else:
                    before_rules[int(rule[0])]=[int(rule[1].strip())]

                if int(rule[1].strip()) in after_rules:
                    after_rules[int(rule[1].strip())].append(int(rule[0]))
                else:
                    after_rules[int(rule[1].strip())]=[int(rule[0])]
            elif line.find(',') > 0:
                updates.append([int(x) for x in line.split(',')])
            else:
                continue
    return (before_rules, after_rules, updates)

if __name__ == '__main__':
    main()