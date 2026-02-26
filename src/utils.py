from typing import List
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


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

def boxplot(df, x_title, y_title, x_col, y_col, save_dir):
    fig1, ax = plt.subplots(figsize=(6, 5))

    sns.boxplot(data=df, x=x_col, y=y_col, ax=ax)
    sns.stripplot(data=df, x=x_col, y=y_col, color="black", size=3, ax=ax)

    ax.set_xlabel(x_title)
    ax.set_ylabel(y_title)

    plt.savefig(save_dir, dpi=300)