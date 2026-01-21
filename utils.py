from typing import List, Tuple
from models import NP, AnalysisResult, GenomicWindow

# Creates list of NPs with just their IDs
def init_nps(np_ids: List[str]) -> List[NP]:
    init_with_ids = []
    
    for np_id in np_ids:
        np = NP(id=np_id, windows=[])
        init_with_ids.append(np)
    
    return init_with_ids

def analyze_data(nuclear_profiles: List[NP], genomic_windows: List[GenomicWindow]):
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

# We use a single function because it's more efficient
# Otherwise, we'd have to iterate over the large dataset multiple times
def analyze_nuclear_profiles(np_data: List[NP]) -> AnalysisResult:
    total_nps = len(np_data)
    total_windows = 0

    # Init to max/min floats
    smallest_num_windows = float('inf')
    largest_num_windows = float('-inf')
    
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