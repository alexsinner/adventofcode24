'''--- Part Two ---

Of course, the secret numbers aren't the prices each buyer is offering! That would be ridiculous. Instead, the prices the buyer offers are just the ones digit of each of their secret numbers.

So, if a buyer starts with a secret number of 123, that buyer's first ten prices would be:

3 (from 123)
0 (from 15887950)
6 (from 16495136)
5 (etc.)
4
4
6
4
4
2

This price is the number of bananas that buyer is offering in exchange for your information about a new hiding spot. However, you still don't speak monkey, so you can't negotiate with the buyers directly. The Historian speaks a little, but not enough to negotiate; instead, he can ask another monkey to negotiate on your behalf.

Unfortunately, the monkey only knows how to decide when to sell by looking at the changes in price. Specifically, the monkey will only look for a specific sequence of four consecutive changes in price, then immediately sell when it sees that sequence.

So, if a buyer starts with a secret number of 123, that buyer's first ten secret numbers, prices, and the associated changes would be:

     123: 3 
15887950: 0 (-3)
16495136: 6 (6)
  527345: 5 (-1)
  704524: 4 (-1)
 1553684: 4 (0)
12683156: 6 (2)
11100544: 4 (-2)
12249484: 4 (0)
 7753432: 2 (-2)

Note that the first price has no associated change because there was no previous price to compare it with.

In this short example, within just these first few prices, the highest price will be 6, so it would be nice to give the monkey instructions that would make it sell at that time. The first 6 occurs after only two changes, so there's no way to instruct the monkey to sell then, but the second 6 occurs after the changes -1,-1,0,2. So, if you gave the monkey that sequence of changes, it would wait until the first time it sees that sequence and then immediately sell your hiding spot information at the current price, winning you 6 bananas.

Each buyer only wants to buy one hiding spot, so after the hiding spot is sold, the monkey will move on to the next buyer. If the monkey never hears that sequence of price changes from a buyer, the monkey will never sell, and will instead just move on to the next buyer.

Worse, you can only give the monkey a single sequence of four price changes to look for. You can't change the sequence between buyers.

You're going to need as many bananas as possible, so you'll need to determine which sequence of four price changes will cause the monkey to get you the most bananas overall. Each buyer is going to generate 2000 secret numbers after their initial secret number, so, for each buyer, you'll have 2000 price changes in which your sequence can occur.

Suppose the initial secret number of each buyer is:

1
2
3
2024

There are many sequences of four price changes you could tell the monkey, but for these four buyers, the sequence that will get you the most bananas is -2,1,-1,3. Using that sequence, the monkey will make the following sales:

    For the buyer with an initial secret number of 1, changes -2,1,-1,3 first occur when the price is 7.
    For the buyer with initial secret 2, changes -2,1,-1,3 first occur when the price is 7.
    For the buyer with initial secret 3, the change sequence -2,1,-1,3 does not occur in the first 2000 changes.
    For the buyer starting with 2024, changes -2,1,-1,3 first occur when the price is 9.

So, by asking the monkey to sell the first time each buyer's prices go down 2, then up 1, then down 1, then up 3, you would get 23 (7 + 7 + 9) bananas!

Figure out the best sequence to tell the monkey so that by looking for that same sequence of changes in every buyer's future prices, you get the most bananas in total. What is the most bananas you can get?
'''


## implementation idea: create a hashmap of sequences and count all the related prices at which to get bananas


def mix(number:int, mix:int):
    '''
    To mix a value into the secret number, calculate the bitwise XOR of the given value and the secret number. Then, the secret number becomes the result of that operation. (If the secret number is 42 and you were to mix 15 into the secret number, the secret number would become 37.)
    '''
    return number ^ mix

def prune(number:int):
    '''
    To prune the secret number, calculate the value of the secret number modulo 16777216. Then, the secret number becomes the result of that operation. (If the secret number is 100000000 and you were to prune the secret number, the secret number would become 16113920.)
    '''
    return number % 16777216

def compute_secrets_prices_changes(number:int, rounds:int):
    '''
    Calculate the secrets as in part 1, then calculate the price as the last number, and change in price by comparing to previous. Returns a list of all secrets, prices, and changes
    Instructions for calculating the secret:
    Calculate the result of multiplying the secret number by 64. Then, mix this result into the secret number. Finally, prune the secret number.
    Calculate the result of dividing the secret number by 32. Round the result down to the nearest integer. Then, mix this result into the secret number. Finally, prune the secret number.
    Calculate the result of multiplying the secret number by 2048. Then, mix this result into the secret number. Finally, prune the secret number.
    Price is the last digit of each secret
    Change is the difference to the previous one
    '''
    previous = number % 10
    results = []
    for i in range(rounds):
        # Calculate the result of multiplying the secret number by 64. Then, mix this result into the secret number. Finally prune the secret number.
        mixer = number * 64
        number = mix(number, mixer)
        number = prune(number)
        # Calculate the result of dividing the secret number by 32. Round the result down to the nearest integer. Then, mix this result into the secret number. Finally, prune the secret number.
        mixer = int(number / 32)
        number = mix(number, mixer)
        number = prune(number)
        # Calculate the result of multiplying the secret number by 2048. Then, mix this result into the secret number. Finally, prune the secret number.
        mixer = number * 2048
        number = mix(number, mixer)
        secret = prune(number)
        price = secret % 10
        change = price - previous
        results.append({'secret':secret, 'price':price, 'change':change})
        previous = price
    return results

def calculate_best_sequence(numbers):
    '''
    Calculate the best sequence of 4 changes to buy the most bananas, given the list of input numbers
    Each buyer only wants to buy one hiding spot, so after the hiding spot is sold, the monkey will move on to the next buyer. If the monkey never hears that sequence of price changes from a buyer, the monkey will never sell, and will instead just move on to the next buyer.
    '''
    sequences = dict() # stores a mapping of each sequence to the total number of bananas bought
    for buyer, number in enumerate(numbers):
        results = compute_secrets_prices_changes(number, 2000)
        for i in range(len(results)-3): 
            sequence = tuple([result['change'] for result in results[i:i+4]])
            price = results[i+3]['price']
            if sequence not in sequences:
                sequences[sequence] = {buyer:price}
            elif buyer in sequences[sequence].keys():
                continue # we only capture the first time the sequence is seen
            else:
                sequences[sequence][buyer] = price
    # now calculate the total bananas bought for each sequence
    for sequence, buyers in sequences.items():
        sequences[sequence] = sum(buyers.values())
    print(f'Bananas: {max(sequences.values())}')

    return sequences

def parse_inputfile(inputfile):
    with open(inputfile) as f:
        return [int(line.strip()) for line in f]
    
def main():
    inputfile = 'data/aoc24_input_22.txt'
    numbers = parse_inputfile(inputfile)
    calculate_best_sequence(numbers)

if __name__ == '__main__':
    main()