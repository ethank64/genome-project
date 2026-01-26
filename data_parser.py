from typing import Tuple, List
import pandas as pd


# Takes the exact tabular structure in data.txt and represents it
# as a pandas data frame. Each row represents a genomic window
def extract_data(file_path: str) -> pd.DataFrame:
    print("Parsing genomic window data...")

    with open(file_path, 'r') as data:
        # Get just the first line (has NPs)
        first_line = data.readline().strip()
        
        # Get all the NP ids
        np_ids = first_line.split('\t')
        np_ids = np_ids[3:]  # Remove the first 3 (not NPs)
        
        # Initialize lists to store data
        starts = []
        stops = []
        np_data = {}

        for np_id in np_ids:
            np_data[np_id] = []
        
        # For each row (genomic window)...
        for genomic_window in data:
            # Get a list of the window data for that row
            start, stop, window_data = parse_row(genomic_window)
            
            starts.append(start)
            stops.append(stop)
            
            # For each NP column ('0' or '1')...
            for i in range(len(window_data)):
                result = window_data[i]
                np_id = np_ids[i]

                # Convert '0'/'1' to bool
                np_data[np_id].append(result == "1")
        
        # Create DataFrame
        df = pd.DataFrame({
            'start': starts,
            'stop': stops,
            **np_data  # Unpack all NP columns
        })
        
        return df

# Takes a row from our data set and returns the start, stop, and list of window data ('0' or '1')
def parse_row(window_row: str) -> Tuple[int, int, List[str]]:
    # Get a list of the window data for that row
    row = window_row.split('\t')

    # Parse where the genomic window starts/stops
    start = int(row[1])
    stop = int(row[2])

    window_data = row[3:]  # Ignore position info

    return start, stop, window_data