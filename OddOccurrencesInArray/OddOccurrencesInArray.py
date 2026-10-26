
def solution(A):
    # Start with zero before checking the array
    result = 0

    # Go through each number in the array
    for num in A:
        # XOR removes matching pairs of numbers
        result ^= num

    # Return the number that has no matching pair
    return result
