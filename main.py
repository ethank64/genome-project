import sys
from utils import analyze_nuclear_profiles, init_nps

def main():
    try:
        with open('./data.txt', 'r') as data:
            print("Initializing nuclear profiles...")
            
            # Get just the first line (has NPs)
            first_line = data.readline().strip()
            
            # Get all the NP ids
            np_ids = first_line.split('\t')
            np_ids = np_ids[3:]  # Remove the first 3 (not NPs)
            
            # Initialize master NP list with IDs
            nuclear_profiles = init_nps(np_ids)
            
            print("Parsing genomic window data...")
            
            total_window_detections = 0
            smallest_window_detection_count = float('inf')
            largest_window_detection_count = float('-inf')
            
            # Parse genomic window data
            genomic_window_count = 0
            
            for genomic_window in data:
                genomic_window = genomic_window.strip()
                if not genomic_window:  # Skip empty lines
                    continue
                
                # Get a list of the window data for that row
                window_data = genomic_window.split('\t')
                window_data = window_data[3:]  # Ignore position info
                
                local_window_detections = 0  # # of windows detected for the current NP
                
                # Update all of our NPs with genomic data
                for i in range(len(window_data)):
                    result = window_data[i]
                    
                    # Update respective NP with window data from that row
                    if result == "0":
                        nuclear_profiles[i].windows.append(False)
                    elif result == "1":
                        nuclear_profiles[i].windows.append(True)
                        local_window_detections += 1
                
                if local_window_detections < smallest_window_detection_count:
                    smallest_window_detection_count = local_window_detections
                if local_window_detections > largest_window_detection_count:
                    largest_window_detection_count = local_window_detections
                
                total_window_detections += local_window_detections
                
                genomic_window_count += 1  # Each row is a genomic window
            
            print("Analyzing data...")
            result = analyze_nuclear_profiles(nuclear_profiles)
            
            print()
            print("=" * 68)
            print(f"Genomic Windows: {genomic_window_count}")
            print(f"Nuclear Profiles: {len(nuclear_profiles)}")
            print(f"Average windows per NP: {result.averageWindowsPerNP}")
            print(f"Smallest # of windows in any NP: {result.smallestWindowCount}")
            print(f"Largest # of windows in any NP: {result.largestWindowCount}")
            print(f"Average NPs in which a window was detected: {total_window_detections / genomic_window_count}")
            print(f"Smallest # of NPs in which a window was detected: {int(smallest_window_detection_count)}")
            print(f"Largest # of NPs in which a window was detected: {int(largest_window_detection_count)}")
            print("=" * 68)
    
    except FileNotFoundError:
        print("Uh oh, data couldn't be loaded!!")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

