from typing import Tuple, List
from models import GenomicWindow, NP


def extract_data(file_path: str) -> Tuple[List[NP], List[GenomicWindow]]:
    print("Parsing genomic window data...")

    with open(file_path, 'r') as data:
        # Get just the first line (has NPs)
        first_line = data.readline().strip()
        
        # Get all the NP ids
        np_ids = first_line.split('\t')
        np_ids = np_ids[3:]  # Remove the first 3 (not NPs)
        
        # Initialize master NP list with IDs
        nuclear_profiles = init_nps(np_ids)

        genomic_windows: List[GenomicWindow] = []
        
        # For each row...
        for genomic_window in data:
            # Get a list of the window data for that row
            start, stop, window_data = parse_row(genomic_window)

            # Track the np ids that show up for this genomic window
            np_ids_for_window: List[str] = []

            # For each column ('0' or '1')...
            for i in range(len(window_data)):
                result = window_data[i]
                
                # Update respective NP with window data from that row
                if result == "0":
                    nuclear_profiles[i].windows.append(False)
                elif result == "1":
                    nuclear_profiles[i].windows.append(True)
                    
                    # Add the NP ID only when the window was detected
                    np_ids_for_window.append(nuclear_profiles[i].id)
            
            genomic_windows.append(GenomicWindow(start=start, stop=stop, NPs=np_ids_for_window))

    return nuclear_profiles, genomic_windows

# Takes a row from our data set and returns the start, stop, and list of window data ('0' or '1')
def parse_row(window_row: str) -> Tuple[int, int, List[str]]:
    # Get a list of the window data for that row
    row = window_row.split('\t')

    # Parse where the genomic window starts/stops
    start = int(row[1])
    stop = int(row[2])

    window_data = row[3:]  # Ignore position info

    return start, stop, window_data

# Creates list of NPs with just their IDs
def init_nps(np_ids: List[str]) -> List[NP]:
    init_with_ids = []
    
    for np_id in np_ids:
        np = NP(id=np_id, windows=[])
        init_with_ids.append(np)
    
    return init_with_ids