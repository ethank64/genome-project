import pandas as pd
from typing import Dict
from collections import Counter
from utils import (
    analyze_data, 
    show_results
)
from subset_extraction import extract_relevant_nps


def analyze_hist1_statistics(hist1_df: pd.DataFrame) -> None:
    # Use activity 1 function to get the stats
    results = analyze_data(hist1_df)
    show_results(results)
    
    # Additional info about relevant NPs
    relevant_nps = extract_relevant_nps(hist1_df)
    print(f"\nRelevant NPs (NPs that detected at least one Hist1 window): {len(relevant_nps)}")
    print("=" * 68)


def analyze_hist1_radial_positions(np_info_df: pd.DataFrame, hist1_df: pd.DataFrame) -> Dict[int, int]:
    print("\n" + "=" * 68)
    print("HIST1 Region Radial Position Stats")
    print("=" * 68)
    
    relevant_nps = extract_relevant_nps(hist1_df)
    
    # Only looks at the relevant nps
    relevant_np_info = np_info_df[np_info_df['np_id'].isin(relevant_nps)]

    # Track all of the discrete rp ratings in a dictionary
    radial_position_counts = Counter(relevant_np_info['radial_position_rating'].values)
    
    # Display results
    print(f"\nNPs that detected Hist1 region: {len(relevant_nps)}")
    print("\nRadial Position Distribution (for NPs that detected Hist1):")
    print("-" * 68)

    for rating in sorted(radial_position_counts.keys()):
        count = radial_position_counts[rating]
        percentage = (count / len(relevant_nps)) * 100
        print(f"Rating {rating}: {count} NPs ({percentage:.1f}%)")
    
    print("\nMost common radial position:")

    if radial_position_counts:
        most_common_rating, count = radial_position_counts.most_common(1)[0]
        print(f"Rating {int(most_common_rating)} with {count} NPs")
    
    print("=" * 68)
    
    return dict(radial_position_counts)


def analyze_hist1_compactions(hist1_df: pd.DataFrame) -> Dict[int, int]:
    print("\n" + "=" * 68)
    print("HIST1 REGION COMPACTION ANALYSIS")
    print("=" * 68)
    
    # hist1_df already has compaction columns since it was extracted from df after compaction was calculated
    compaction_ratings = hist1_df['compaction_rating'].dropna()
    compaction_values = hist1_df['compaction'].dropna()
    
    compaction_rating_counts = Counter(compaction_ratings.values)
    avg_compaction = compaction_values.mean()
    
    # Display results
    print(f"\nNumber of Hist1 windows analyzed: {len(compaction_ratings)}")
    print(f"Average compaction value: {avg_compaction:.4f}")
    print("\nCompaction Rating Distribution:")
    print("-" * 68)

    for rating in sorted(compaction_rating_counts.keys()):
        count = compaction_rating_counts[rating]
        percentage = (count / len(compaction_ratings)) * 100
        print(f"Rating {rating}: {count} windows ({percentage:.1f}%)")
    
    print("\nMost common compaction rating:")
    
    if compaction_rating_counts:
        most_common_rating, count = compaction_rating_counts.most_common(1)[0]
        print(f"Rating {int(most_common_rating)} with {count} windows")
    
    print("=" * 68)
    
    return dict(compaction_rating_counts)

