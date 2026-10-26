
def solution(X, Y, D):
    # Calculate the total distance the frog needs to travel
    distance = Y - X

    # Calculate the minimum number of jumps
    # Round up because the frog must reach or pass Y
    jumps = (distance + D - 1) // D

    # Return the minimum number of jumps
    return jumps
