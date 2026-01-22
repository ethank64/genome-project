import matplotlib.pyplot as plt
from models import NP
import numpy as nump
from typing import List
from collections import Counter

def plot_radial_position(nuclear_profiles: List[NP]):
    # Extract original values and ratings
    detection_frequencies = nump.array([np.detection_frequency for np in nuclear_profiles])
    radial_position_ratings = nump.array([np.radial_position_rating for np in nuclear_profiles])
    
    # Create side-by-side subplots
    fig, (left, right) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Left plot: Histogram of detection frequency (continuous values)
    left.hist(detection_frequencies, bins=30, edgecolor='black')
    left.set_xlabel("Detection Frequency")
    left.set_ylabel("Number of Nuclear Profiles")
    left.set_title("Distribution of Detection Frequency")
    left.grid(True, alpha=0.3)
    
    # Right plot: Bar chart of ratings (discrete values)
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