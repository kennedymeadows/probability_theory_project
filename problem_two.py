import argparse
import numpy as np
import math

def shannon_entropy(sequence):
    """ Calculate Shannon Entropy for a binary sequence """
    p = sequence.count('1') / len(sequence)
    if p == 0 or p == 1:  # To handle cases where p is 0 or 1
        return 0
    return -p * math.log2(p) - (1 - p) * math.log2(1 - p)

def monobit_test(sequence):
    """ Frequency (monobit) test """
    count = sequence.count('1') - sequence.count('0')
    return abs(count) / len(sequence)

def runs_test(sequence):
    """ Runs test """
    runs = 1
    for i in range(len(sequence) - 1):
        if sequence[i] != sequence[i + 1]:
            runs += 1
    return runs

def autocorrelation_test(sequence, shift=2):
    """ Autocorrelation test """
    match = 0
    for i in range(len(sequence) - shift):
        if sequence[i] == sequence[i + shift]:
            match += 1
    return match / (len(sequence) - shift)

def longest_run_of_ones_test(sequence, default_block_size=128):
    """ Longest Run of Ones in a Block Test """
    # Adjust block size for shorter sequences
    block_size = default_block_size
    while len(sequence) < block_size and block_size > 1:
        block_size //= 2

    num_blocks = len(sequence) // block_size
    if num_blocks == 0:
        return None, None

    longest_runs = []
    for i in range(num_blocks):
        block = sequence[i * block_size:(i + 1) * block_size]
        max_run = max(map(len, block.split('0')))
        longest_runs.append(max_run)

    return np.mean(longest_runs)

def poker_test(sequence, block_size=4):
    """ Poker Test """
    if len(sequence) < block_size:
        return None

    # Divide the sequence into blocks and count the occurrences
    block_counts = {}
    num_blocks = len(sequence) // block_size
    for i in range(num_blocks):
        block = sequence[i * block_size:(i + 1) * block_size]
        block_counts[block] = block_counts.get(block, 0) + 1

    # Calculate the test statistic
    test_statistic = (2**block_size) * sum(v**2 for v in block_counts.values()) / num_blocks - num_blocks
    return test_statistic

####################################################################################################
####################### Random/ Non-Random Sequence Generators #####################################
####################################################################################################

def generate_champernowne(length):
    """ Generate a binary string representing the Champernowne constant up to a certain length """
    champernowne = ""
    num = 1
    while len(champernowne) < length:
        champernowne += bin(num)[2:]  # Remove '0b' prefix from binary representation
        num += 1
    return champernowne[:length]

def is_prime(n):
    """ Check if a number is prime """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_copeland_erdos(length):
    """ Generate a binary string representing the Copeland-Erdös constant up to a certain length """
    copeland_erdos = ""
    num = 2  # Start from the first prime number
    while len(copeland_erdos) < length:
        if is_prime(num):
            copeland_erdos += bin(num)[2:]  # Remove '0b' prefix from binary representation
        num += 1
    return copeland_erdos[:length]

def generate_non_random_binary(length, pattern="1100"):
    """ Generate a non-random binary string with a specified pattern """
    return (pattern * (length // len(pattern) + 1))[:length]


####################################################################################################
##################################### Sequence Analyzer ############################################
####################################################################################################


def interpret_results(sequence, freq, runs, autocorr, longest_run_mean, poker_test_result, entropy):
    """ Interpret the results and provide a conclusion about randomness """
    sequence_length = len(sequence)

    # Adjust weights based on sequence length
    weights = {
        'freq': 0.2,
        'runs': 0 if sequence_length < 50 else 0.2,  # Reduced importance for short sequences
        'autocorr': 0.2,
        'longest_run': 0.2,
        'poker_test': 0.2,
        'entropy': 0.3 
    }

    freq_threshold = 0.2  
    runs_threshold = 15 if sequence_length < 100 else 30  # Lower threshold for shorter sequences
    autocorr_threshold = 0.15 
    longest_run_mean_threshold = 3 if sequence_length < 100 else 4  # Adjusted for length
    poker_test_threshold = 3.0 
    entropy_threshold = 0.7  

    # Calculate weighted score
    score = 0
    score += weights['freq'] if freq < freq_threshold else 0
    score += weights['runs'] if runs > runs_threshold else 0
    score += weights['autocorr'] if autocorr < autocorr_threshold else 0
    score += weights['longest_run'] if longest_run_mean < longest_run_mean_threshold else 0
    score += weights['poker_test'] if poker_test_result < poker_test_threshold else 0
    score += weights['entropy'] if entropy > entropy_threshold else 0

    return f"The sequence is likely random. The score was {score}" if score >= 0.6 else f"The sequence is likely not random. The score was {score}"

def analyze_sequence(sequence, print_sequence=True):
    """ Analyze the sequence with various tests and print results """
    sequence = sequence.replace(" ", "")  # Remove spaces
    if print_sequence:
        print("Analyzing sequence:", sequence)
    
    freq_result = monobit_test(sequence)
    runs_result = runs_test(sequence)
    autocorr_result = autocorrelation_test(sequence)
    longest_run_mean = longest_run_of_ones_test(sequence)
    poker_test_result = poker_test(sequence)
    entropy_result = shannon_entropy(sequence)

    print("Frequency (Monobit) Test Result:", freq_result)
    print("Runs Test Result:", runs_result)
    print("Autocorrelation Test Result (Shift=2):", autocorr_result)
    print("Longest Run of Ones in a Block Test Result (Block Size=128):", longest_run_mean)
    print("Poker Test Result (Block Size=4):", poker_test_result)
    print("Shannon Entropy:", entropy_result)

    # conclusion = interpret_results(sequence, freq_result, runs_result, autocorr_result, longest_run_mean, poker_test_result, entropy_result)
    # print("Conclusion:", conclusion)

def main():
    parser = argparse.ArgumentParser(description="Randomness Test CLI")
    parser.add_argument('--test', type=str, help='Binary sequence to test for randomness')
    parser.add_argument('--generate-champernowne', type=int, help='Generate Champernowne constant up to a length')
    parser.add_argument('--generate-copeland-erdos', type=int, help='Generate Copeland-Erdös constant up to a length')
    parser.add_argument('--generate-nonrandom', type=int, help='Generate a non-random binary string of a length')
    parser.add_argument('--no-print-sequence', action='store_true', help='Do not print the sequence')
    args = parser.parse_args()

    if args.test:
        analyze_sequence(args.test, not args.no_print_sequence)
    elif args.generate_champernowne:
        sequence = generate_champernowne(args.generate_champernowne)
        analyze_sequence(sequence, not args.no_print_sequence)
    elif args.generate_copeland_erdos:
        sequence = generate_copeland_erdos(args.generate_copeland_erdos)
        analyze_sequence(sequence, not args.no_print_sequence)
    elif args.generate_nonrandom:
        sequence = generate_non_random_binary(args.generate_nonrandom)
        analyze_sequence(sequence, not args.no_print_sequence)
    else:
        print("Randomness Test CLI")
        print("Usage: python problem_two.py --test 'BINARY_SEQUENCE'")
        print("Example: python problem_two.py --test '0101 0101'")
        print("Or generate sequences:")
        print("python problem_two.py --generate-champernowne 100")
        print("python problem_two.py --generate-copeland-erdos 100")
        print("python problem_two.py --generate-nonrandom 100")

if __name__ == "__main__":
    main()