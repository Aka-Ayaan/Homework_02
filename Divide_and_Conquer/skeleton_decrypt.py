# Decrypts the data using the logic of the Karatsuba algorithm.
# Args:
#   data: List of list consisting leaves
# Returns:
#   A tuple containing the original two numbers.
def reverse_karatsuba(data) -> tuple:
        
    first = data[0]
    last = data[-1]

    # If the first element is a list, then it is a leaf node
    if isinstance(data[0], list):
        first = reverse_karatsuba(first)
    
    # If the last element is a list, then it is a leaf node
    if isinstance(data[-1], list):
        last = reverse_karatsuba(last)
    
    return (((last[0] * (10 ** len(str(first[0])))) + first[0]), ((last[1] * (10 ** len(str(first[1])))) + first[1]))

# This function reads data from a specified file and decrypt data using the logic of the Karatsuba algorithm.
# Args:
#   filename: The name of the file containing input data.
# Returns:
#   A list of tuples, each tuple representing coordinates (x, y).
def main(filename) -> list[tuple[int, int]]:

    # Read data from the file
    data = []
    with open(filename, 'r') as file:
        for line in file:
            data.append(eval(line.strip()))

    n = data[:1][0]
    data = data[1:]

    # Decrypt the data
    result = []
    for i in range(n):
        result.append(reverse_karatsuba(data[i]))

    return result

# if __name__ == '__main__':
#     main('input_decrypt.txt')
#     x = [[(2, 1), (6, 10), (4, 9)], [(2, 8), (6, 20), (4, 12)], (0, 37)]
#     print(reverse_karatsuba(x))