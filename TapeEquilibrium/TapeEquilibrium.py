
def solution(A):
    # Calculate the sum of all elements in the array
    total_sum = sum(A)

    # Initialize the sum of the left part
    left_sum = 0

    # Start with an infinitely large difference
    min_diff = float('inf')

    # Check every possible split into two non-empty parts
    for i in range(len(A) - 1):

        # Add the current element to the left part
        left_sum += A[i]

        # Calculate the sum of the right part
        right_sum = total_sum - left_sum

        # Find the absolute difference between the two parts
        diff = abs(left_sum - right_sum)

        # Update the minimum difference if necessary
        if diff < min_diff:
            min_diff = diff

    # Return the smallest absolute difference
    return min_diff
