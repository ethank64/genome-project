from typing import List
import random


# Implements p5.js's map function to take a value from one range to another
def map_range(value, in_min, in_max, out_min, out_max):
    value = clamp(value, in_min, in_max)

    # Round the value to make it discrete
    return round((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def clamp(value, low, high):
    return max(low, min(value, high))


def random_subset(arr: List, k: int) -> List:
    universal_set = arr.copy()
    subset = []
    
    for i in range(k):
        item = random.choice(universal_set)
        subset.append(item)
        universal_set.remove(item)

    return subset


def create_2d_array(cols: int) -> List[List]:
    array = []

    for i in range(cols):
        array.append([])

    return array