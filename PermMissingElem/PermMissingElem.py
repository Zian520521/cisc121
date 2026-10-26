
def solution(A):
    # Get the number of elements in the array
    N = len(A)

    # Calculate the expected sum from 1 to N + 1
    expected_sum = (N + 1) * (N + 2) // 2

    # Calculate the sum of the existing elements
    actual_sum = sum(A)

    # Find the missing number by subtracting the sums
    missing_number = expected_sum - actual_sum

    # Return the missing number
    return missing_number
