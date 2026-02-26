from typing import List
import random
import numpy as np
import matplotlib.pyplot as plt


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

def plot_radar(labels, values, title, save_dir):
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()

    angles_closed = angles + angles[:1]
    ratios_closed = values + values[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    ax.plot(angles_closed, ratios_closed, linewidth=2)
    ax.fill(angles_closed, ratios_closed, alpha=0.25)

    ax.set_xticks(angles)
    ax.set_xticklabels(labels)

    ax.set_title(title)
    ax.set_ylim(0, 1)

    plt.savefig(save_dir, dpi=300)