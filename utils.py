import pandas as pd
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



def fill_in_radial_position(df: pd.DataFrame, min_rating: int, max_rating: int) -> pd.DataFrame:
    known_non_np_columns = ['chrom', 'start', 'stop', 'compaction', 'compaction_rating']
    np_columns = [col for col in df.columns if col not in known_non_np_columns]
    total_genomic_windows = len(df)
    
    detection_frequencies = {}
    for np_id in np_columns:
        # Sum of True values / total windows
        detection_freq = df[np_id].sum() / total_genomic_windows
        detection_frequencies[np_id] = detection_freq
    
    freq_values = list(detection_frequencies.values())
    data_min = min(freq_values)
    data_max = max(freq_values)
    
    # Calculate radial position ratings
    radial_position_ratings = {}
    for np_id, detection_freq in detection_frequencies.items():
        rating = map_range(detection_freq, data_min, data_max, min_rating, max_rating)
        radial_position_ratings[np_id] = rating
    
    # Return a DataFrame with NP info
    np_info_df = pd.DataFrame({
        'np_id': list(detection_frequencies.keys()),
        'detection_frequency': list(detection_frequencies.values()),
        'radial_position_rating': list(radial_position_ratings.values())
    })
    
    return np_info_df



def fill_in_compaction(df: pd.DataFrame, min_rating: int, max_rating: int) -> pd.DataFrame:
    known_non_np_columns = ['chrom', 'start', 'stop', 'compaction', 'compaction_rating']
    np_columns = [col for col in df.columns if col not in known_non_np_columns]
    total_nps = len(np_columns)
    
    df['compaction'] = 1 - df[np_columns].sum(axis=1) / total_nps
    
    # Hard-coded. Probably not the best, but otherwise we get weird numbers
    # I got this from looking at the raw compaction data. Seems like there's some
    # extreme outliers past this value to the left
    data_min = 0.853
    data_max = df['compaction'].max()
    
    # Map the actual compaction to a value between our selected range
    # The process is manual, but it helps take the outliers out of the equation
    df['compaction_rating'] = df['compaction'].apply(
        lambda x: map_range(x, data_min, data_max, min_rating, max_rating)
    )
    
    return df


