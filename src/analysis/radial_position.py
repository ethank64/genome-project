import pandas as pd
from utils import map_range

def fill_in_radial_position(df: pd.DataFrame, min_rating: int, max_rating: int) -> pd.DataFrame:
    known_non_np_columns = ['chrom', 'start', 'stop', 'compaction', 'compaction_rating']
    np_columns = [col for col in df.columns if col not in known_non_np_columns]
    total_genomic_windows = len(df)
    
    detection_frequencies = {}
    for np_id in np_columns:
        data = df[np_id].to_list()

        total_matches = 0

        for window in data:
            if window:
                total_matches += 1

        detection_freq = total_matches / total_genomic_windows
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