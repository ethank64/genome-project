import matplotlib.pyplot as plt
from models import NP, ClusterSet
import pandas as pd
from typing import List
from analysis.radial_position import fill_in_radial_position
from constants import GRAPHS_DIR

def plot_cluster_radial_positions(cluster_set: ClusterSet, region: pd.DataFrame):
    clusters = cluster_set.clusters

    for medoid in clusters:
        nps: List[NP] = clusters[medoid]
        np_ids: List[str] = [np.np_id for np in nps]

        cluster_subset = region[np_ids]

        radial_position_df = fill_in_radial_position(cluster_subset, 1, 5)

        plot_radial_position(radial_position_df, medoid)

def plot_radial_position(np_info_df: pd.DataFrame, medoid_id: str):
    # Extract values
    detection_frequencies = np_info_df['detection_frequency'].values
    radial_position_ratings = np_info_df['radial_position_rating'].values
    
    # Create side-by-side subplots
    fig, (left, right) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Left plot: Histogram of detection frequency (continuous values)
    left.hist(detection_frequencies, bins=30, edgecolor='black')
    left.set_xlabel("Detection Frequency")
    left.set_ylabel("Number of Nuclear Profiles")
    left.set_title(f"Distribution of Detection Frequency ({medoid_id})")
    left.grid(True, alpha=0.3)
    
    # Right plot: Bar chart of ratings (discrete values)
    from collections import Counter
    rating_counts = Counter(radial_position_ratings)
    ratings = sorted(rating_counts.keys())
    counts = [rating_counts[rating] for rating in ratings]
    
    right.bar(ratings, counts, edgecolor='black')
    right.set_xlabel("Radial Position Rating")
    right.set_ylabel("Number of Nuclear Profiles")
    right.set_title(f"Distribution of Radial Position Ratings ({medoid_id})")
    right.set_xticks(ratings)
    right.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    GRAPHS_DIR.mkdir(parents=True, exist_ok=True)
    file_name = "radial_positions_" + medoid_id
    plt.savefig(GRAPHS_DIR / file_name, dpi=300)