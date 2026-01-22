import matplotlib.pyplot as plt
from models import GenomicWindow
import numpy as nump
from typing import List
from collections import Counter

def plot_compaction(genomic_windows: List[GenomicWindow]):
    # Extract original values and ratings
    compaction_values = nump.array([window.compaction for window in genomic_windows])
    compaction_ratings = nump.array([window.compaction_rating for window in genomic_windows])
    
    # Create side-by-side subplots
    fig, (left, right) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Left plot: Histogram of compaction (continuous values)
    left.hist(compaction_values, bins=100, edgecolor='black')
    left.set_xlabel("Compaction")
    left.set_ylabel("Number of Windows")
    left.set_title("Distribution of Compaction Values")
    left.grid(True, alpha=0.3)
    
    # Right plot: Bar chart of ratings (discrete values)
    rating_counts = Counter(compaction_ratings)
    ratings = sorted(rating_counts.keys())
    counts = [rating_counts[rating] for rating in ratings]
    
    right.bar(ratings, counts, edgecolor='black')
    right.set_xlabel("Compaction Rating")
    right.set_ylabel("Number of Windows")
    right.set_title("Distribution of Compaction Ratings")
    right.set_xticks(ratings)
    right.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.show()