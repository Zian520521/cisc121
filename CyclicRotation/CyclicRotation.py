class Solution:
    def solution(self, A, K):
        # Get the length of the array
        N = len(A)

        # Return the original array if it is empty
        if N == 0:
            return A

        # Create a new array to store the rotated elements
        result = [0] * N

        # Calculate the effective number of rotations
        K = K % N

        # Move each element to its new position
        for i in range(N):
            newIndex = (i + K) % N
            result[newIndex] = A[i]

        # Return the rotated array
        return result
