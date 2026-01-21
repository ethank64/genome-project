from typing import List
from models import NP, AnalysisResult

# Creates list of NPs with just their IDs
def init_nps(np_ids: List[str]) -> List[NP]:
    init_with_ids = []
    
    for np_id in np_ids:
        np = NP(id=np_id, windows=[])
        init_with_ids.append(np)
    
    return init_with_ids


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
    
    result = AnalysisResult(
        averageWindowsPerNP=total_windows / total_nps,
        smallestWindowCount=int(smallest_num_windows),
        largestWindowCount=int(largest_num_windows)
    )
    
    return result
