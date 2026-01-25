import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_compaction(df: pd.DataFrame):
    """
    Plot compaction data from DataFrame.
    
    Args:
        df: DataFrame with 'compaction' and 'compaction_rating' columns
    """
    # Extract values
    compaction_values = df['compaction'].values
    compaction_ratings = df['compaction_rating'].values
    
    # Create side-by-side subplots
    fig, (left, right) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Left plot: Histogram of compaction (continuous values)
    left.hist(compaction_values, bins=100, edgecolor='black')
    left.set_xlabel("Compaction")
    left.set_ylabel("Number of Windows")
    left.set_title("Distribution of Compaction Values")
    left.grid(True, alpha=0.3)
    
    # Right plot: Bar chart of ratings (discrete values)
    from collections import Counter
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