def rng(x, a, b):
    return (x*a+b) & ((2**56)-1)

def gen_random(seed, a, b):
    state = seed
    while True:
        state = rng(state, a, b)
        yield state & 0xFF

def verify_seed(seed, a, b, random_numbers):
    """
    Modular arithmetic has the following property for both addition
    and multiplication:
    (a * b) % c = (a % c * b % c)

    We can abuse that because in the process of masking the number 
    with 0xFF we're essentially doing the above operation. What that
    means is we can ignore the other 48 bits of A, B, and SEED and 
    focus on just brute-forcing the last 8 bits for each. Leaving
    us only 256 * 256 * 256 = 16,777,216 permuations to test. We 
    can do so just by checking the first five numbers of the generator
    and making sure they match with the result of the flag starting
    with CSCG{
    """
    flag = "CSCG{"
    flag_bytes = [ord(char) for char in flag]
    generator = gen_random(seed, a, b)

    for random_number, flag_byte in zip(random_numbers, flag_bytes):
        if next(generator) != (random_number ^ flag_byte):
            return False
    return True


if __name__ == "__main__":
    with open("msg.txt", "r") as f:
        program_output = f.readlines()
    
    # parse random numbers
    random_numbers = [int(line.strip()) for line in program_output[1:]]

    # recover original seed
    for seed in range(125, 0xFF):
        print(f"Trying all combinations of a and b with seed {seed}.")
        for a in range(0, 0xFF):
            for b in range(0, 0xFF):
                if verify_seed(seed, a, b, random_numbers[0:5]):
                    print(f"Found initial state\na: {a}\nb: {b}\nseed:{seed}")
                    generator = gen_random(seed, a, b)
                    flag_bytes = [next(generator) ^ random_number for random_number in random_numbers]
                    print(f"Flag: {''.join(chr(flag_byte) for flag_byte in flag_bytes)}")
                    exit()