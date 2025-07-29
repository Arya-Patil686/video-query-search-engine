import numpy as np

def euclidean_distance(a, b):
    return np.sum((np.array(a) - np.array(b)) ** 2)

def find_min_distance_index(longer_array, shorter_array):
    n = len(longer_array)
    k = len(shorter_array)

    if n <= k:
        return -1  # No solution if the longer array is not longer than the shorter one

    min_distance = k + 1 #float('inf')
    min_index = -1

    for i in range(n - k + 1):
        window = longer_array[i:i+k]
        distance = euclidean_distance(window, shorter_array)
        if distance < min_distance:
            min_distance = distance
            min_index = i

    return min_index

if __name__ == "__main__":
    # Example usage
    longer_array = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    shorter_array = [2, 3, 4]
    index = find_min_distance_index(longer_array, shorter_array)
    print("Index:", index)
