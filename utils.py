from typing import List
from models import NP, AnalysisResult, GenomicWindow
import statistics


# DF is basically how often windows showed up / total windows
def fill_in_radial_position(nuclear_profiles: List[NP], total_genomic_windows: int, min_rating, max_rating):
    # First pass: calculate all detection frequencies
    detection_frequencies = []
    for np in nuclear_profiles:
        local_window_count = 0

        # Count up all the windows (1s) for this NP
        for window in np.windows:
            if window:
                local_window_count += 1

        # Calculate and set the detection frequency
        df = local_window_count / total_genomic_windows
        np.detection_frequency = df
        detection_frequencies.append(df)
    
    
    data_min = min(detection_frequencies)
    data_max = max(detection_frequencies)
    
    # Map the detection frequency to a discrete rating
    for np in nuclear_profiles:
        np.radial_position_rating = map_range(np.detection_frequency, data_min, data_max, min_rating, max_rating)

# Compaction is basically the inverse of how spread out it is (which is the ratio of found / total)
def fill_in_compaction(genomic_windows: List[GenomicWindow], total_nps: int, min_rating, max_rating):
    # First pass: calculate all compaction values
    compaction_values = []
    for window in genomic_windows:
        local_np_count = len(window.NPs)

        # If it showed up less -> higher compaction
        compaction = 1 - local_np_count / total_nps
        window.compaction = compaction
        compaction_values.append(compaction)
    
    # Hard-coded. Probably not the best, but otherwise we get weird numbers
    # I got this from looking at the raw compaction data. Seems like there's some
    # extreme outliers past this value to the left
    data_min = 0.853
    data_max = max(compaction_values)
    
    # Map the actual compaction to a value between our selected range
    # The process is manual, but it helps take the outliers out of the equation
    for window in genomic_windows:
        window.compaction_rating = map_range(window.compaction, data_min, data_max, min_rating, max_rating)


# Implements p5.js's map function to take a value from one range to another
def map_range(value, in_min, in_max, out_min, out_max):
    value = clamp(value, in_min, in_max)

    # Round the value to make it discrete
    return round((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def clamp(value, low, high):
    return max(low, min(value, high))










# Legacy code from activity 1
def analyze_data(nuclear_profiles: List[NP], genomic_windows: List[GenomicWindow]):
    print("Analyzing data...")
    average_windows_per_np, smallest_window_count, largest_window_count = analyze_nuclear_profiles(nuclear_profiles)
    average_nps_per_window, smallest_np_count, largest_np_count = analyze_genomic_windows(genomic_windows)

    return AnalysisResult(
        window_count=len(genomic_windows),
        np_count=len(nuclear_profiles),
        average_windows_per_np=average_windows_per_np,
        smallest_window_count=smallest_window_count,
        largest_window_count=largest_window_count,
        average_nps_per_window=average_nps_per_window,
        smallest_np_count=smallest_np_count,
        largest_np_count=largest_np_count
    )


def analyze_nuclear_profiles(np_data: List[NP]) -> AnalysisResult:
    total_nps = len(np_data)
    total_windows = 0

    # Init to max/min floats
    smallest_num_windows = float('inf')
    largest_num_windows = float('-inf')
    
    # For each nuclear profile...
    for np in np_data:
        local_window_count = 0  # Tracks the number of windows for that np
        
        # Count the number of windows
        for window in np.windows:
            # If the window is truthy (1)
            if window:
                local_window_count += 1
        
        if local_window_count < smallest_num_windows:
            smallest_num_windows = local_window_count
        if local_window_count > largest_num_windows:
            largest_num_windows = local_window_count
        
        total_windows += local_window_count

    average_windows_per_np = total_windows / total_nps
    smallest_window_count = int(smallest_num_windows)
    largest_window_count = int(largest_num_windows)
    
    return average_windows_per_np, smallest_window_count, largest_window_count

def analyze_genomic_windows(genomic_windows: List[GenomicWindow]) -> AnalysisResult:
    total_windows = len(genomic_windows)
    total_nps = 0

    smallest_num_nps = float('inf')
    largest_num_nps = float('-inf')

    for window in genomic_windows:
        local_np_count = len(window.NPs)

        if local_np_count < smallest_num_nps:
            smallest_num_nps = local_np_count
        if local_np_count > largest_num_nps:
            largest_num_nps = local_np_count

        total_nps += local_np_count

    average_nps_per_window = total_nps / total_windows
    smallest_np_count = smallest_num_nps
    largest_np_count = largest_num_nps

    return average_nps_per_window, smallest_np_count, largest_np_count

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