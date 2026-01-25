import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_radial_position(np_info_df: pd.DataFrame):
    """
    Plot radial position data from NP info DataFrame.
    
    Args:
        np_info_df: DataFrame with columns 'np_id', 'detection_frequency', 'radial_position_rating'
    """
    # Extract values
    detection_frequencies = np_info_df['detection_frequency'].values
    radial_position_ratings = np_info_df['radial_position_rating'].values
    
    # Create side-by-side subplots
    fig, (left, right) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Left plot: Histogram of detection frequency (continuous values)
    left.hist(detection_frequencies, bins=30, edgecolor='black')
    left.set_xlabel("Detection Frequency")
    left.set_ylabel("Number of Nuclear Profiles")
    left.set_title("Distribution of Detection Frequency")
    left.grid(True, alpha=0.3)
    
    # Right plot: Bar chart of ratings (discrete values)
    from collections import Counter
    rating_counts = Counter(radial_position_ratings)
    ratings = sorted(rating_counts.keys())
    counts = [rating_counts[rating] for rating in ratings]
    
    right.bar(ratings, counts, edgecolor='black')
    right.set_xlabel("Radial Position Rating")
    right.set_ylabel("Number of Nuclear Profiles")
    right.set_title("Distribution of Radial Position Ratings")
    right.set_xticks(ratings)
    right.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.show()