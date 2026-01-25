from models import AnalysisResult
import pandas as pd
from typing import List


# DF is basically how often windows showed up / total windows
def fill_in_radial_position(df: pd.DataFrame, min_rating: int, max_rating: int) -> pd.DataFrame:
    """
    Calculate detection frequency and radial position rating for each NP.
    
    Returns a DataFrame with NP info: 'np_id', 'detection_frequency', 'radial_position_rating'
    """
    # Get NP columns (all columns except known non-NP columns)
    known_non_np_columns = ['start', 'stop', 'compaction', 'compaction_rating']
    np_columns = [col for col in df.columns if col not in known_non_np_columns]
    total_genomic_windows = len(df)
    
    # Calculate detection frequencies for each NP
    detection_frequencies = {}
    for np_id in np_columns:
        # Sum of True values / total windows
        detection_freq = df[np_id].sum() / total_genomic_windows
        detection_frequencies[np_id] = detection_freq
    
    # Find min and max detection frequencies
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

# Compaction is basically the inverse of how spread out it is (which is the ratio of found / total)
def fill_in_compaction(df: pd.DataFrame, min_rating: int, max_rating: int) -> pd.DataFrame:
    """
    Calculate compaction and compaction rating for each genomic window.
    
    Returns the DataFrame with added 'compaction' and 'compaction_rating' columns.
    """
    # Get NP columns (all columns except known non-NP columns)
    known_non_np_columns = ['start', 'stop', 'compaction', 'compaction_rating']
    np_columns = [col for col in df.columns if col not in known_non_np_columns]
    total_nps = len(np_columns)
    
    # Calculate compaction for each window (row)
    # Compaction = 1 - (number of NPs where window was detected / total NPs)
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


# Implements p5.js's map function to take a value from one range to another
def map_range(value, in_min, in_max, out_min, out_max):
    value = clamp(value, in_min, in_max)

    # Round the value to make it discrete
    return round((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def clamp(value, low, high):
    return max(low, min(value, high))






# Legacy code from activity 1
def analyze_data(df: pd.DataFrame) -> AnalysisResult:
    """
    Analyze the genomic window data DataFrame.
    
    Returns an AnalysisResult with statistics about windows and nuclear profiles.
    """
    print("Analyzing data...")
    average_windows_per_np, smallest_window_count, largest_window_count = analyze_nuclear_profiles(df)
    average_nps_per_window, smallest_np_count, largest_np_count = analyze_genomic_windows(df)

    # Get NP columns to count total NPs
    known_non_np_columns = ['start', 'stop', 'compaction', 'compaction_rating']
    np_columns = [col for col in df.columns if col not in known_non_np_columns]

    return AnalysisResult(
        window_count=len(df),
        np_count=len(np_columns),
        average_windows_per_np=average_windows_per_np,
        smallest_window_count=smallest_window_count,
        largest_window_count=largest_window_count,
        average_nps_per_window=average_nps_per_window,
        smallest_np_count=smallest_np_count,
        largest_np_count=largest_np_count
    )


def analyze_nuclear_profiles(df: pd.DataFrame):
    """
    Analyze nuclear profiles from DataFrame.
    
    Returns: (average_windows_per_np, smallest_window_count, largest_window_count)
    """
    # Filter out just the np_columns
    non_np_columns: List[str] = ['start', 'stop', 'compaction', 'compaction_rating']
    np_columns: List[str] = [col for col in df.columns if col not in non_np_columns]
    total_nps: int = len(np_columns)
    
    # Count windows (True values) for each NP
    window_counts = df[np_columns].sum()  # Series with window count per NP
    
    total_windows = window_counts.sum()
    smallest_num_windows = int(window_counts.min())
    largest_num_windows = int(window_counts.max())
    
    average_windows_per_np = total_windows / total_nps
    
    return average_windows_per_np, smallest_num_windows, largest_num_windows

def analyze_genomic_windows(df: pd.DataFrame):
    """
    Analyze genomic windows from DataFrame.
    
    Returns: (average_nps_per_window, smallest_np_count, largest_np_count)
    """
    # Get NP columns (all columns except known non-NP columns)
    known_non_np_columns = ['start', 'stop', 'compaction', 'compaction_rating']
    np_columns = [col for col in df.columns if col not in known_non_np_columns]
    
    total_windows = len(df)
    
    # Count NPs (True values) for each window (row)
    np_counts = df[np_columns].sum(axis=1)  # Series with NP count per window
    
    total_nps = np_counts.sum()
    smallest_num_nps = int(np_counts.min())
    largest_num_nps = int(np_counts.max())
    
    average_nps_per_window = total_nps / total_windows
    
    return average_nps_per_window, smallest_num_nps, largest_num_nps

def show_results(results: AnalysisResult):
    print()
    print("=" * 68)
    print(f"Genomic Windows: {results.window_count}")
    print(f"Nuclear Profiles: {results.np_count}")
    print(f"Average windows per NP: {results.average_windows_per_np}")
    print(f"Smallest # of windows in any NP: {results.smallest_window_count}")
    print(f"Largest # of windows in any NP: {results.largest_window_count}")
    print(f"Average NPs in which a window was detected: {results.average_nps_per_window}")
    print(f"Smallest # of NPs in which a window was detected: {results.smallest_np_count}")
    print(f"Largest # of NPs in which a window was detected: {results.largest_np_count}")
    print("=" * 68)