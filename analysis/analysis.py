from models import AnalysisResult
import pandas as pd
from typing import List

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
    known_non_np_columns = ['chrom', 'start', 'stop', 'compaction', 'compaction_rating']
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
    non_np_columns: List[str] = ['chrom', 'start', 'stop', 'compaction', 'compaction_rating']
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
    known_non_np_columns = ['chrom', 'start', 'stop', 'compaction', 'compaction_rating']
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