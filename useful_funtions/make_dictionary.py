import itertools

def generate_combinations(charset, length):
    # Generate all combinations of given length using the charset
    for attempt in itertools.product(charset, repeat=length):
        yield ''.join(attempt)

def save_combinations_to_file(charset, length, file_path):
    with open(file_path, 'w') as file:
        for combination in generate_combinations(charset, length):
            file.write(combination + '\n')
    print(f"All combinations of length {length} have been saved to '{file_path}'.")

# Example usage
if __name__ == "__main__":
    charset = "aimvy"
    length = 6  # Change this to the length you want to generate combinations for
    file_path = 'F:\PassHunter\distionary.txt'  # Path to save the combinations

    save_combinations_to_file(charset, length, file_path)
