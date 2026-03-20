from typing import List
import pandas as pd


def get_normalized_linkage_table(region: pd.DataFrame) -> pd.DataFrame:
    window_starts: List[int] = region['start'].tolist()

    df = pd.DataFrame(index=window_starts, columns=window_starts)

    df_cache = {}

    for window_start in window_starts:
        window_df = get_window_detection_frequency(region, window_start)
        df_cache[window_start] = window_df

    for window_start in window_starts:
        for other_window_start in window_starts:
            df_a = df_cache[window_start]
            df_b = df_cache[other_window_start]
            cosegregation = get_cosegregation(region, window_start, other_window_start)
            normalized_linkage = calculate_normalized_linkage(df_a, df_b, cosegregation)
            
            df.loc[window_start, other_window_start] = normalized_linkage

    return df



def get_window_detection_frequency(region: pd.DataFrame, window_start: int):
    known_non_np_columns = ['chrom', 'start', 'stop', 'compaction', 'compaction_rating']
    np_columns = [col for col in region.columns if col not in known_non_np_columns]

    total_nps = len(np_columns)
    window_starts: List[int] = region['start'].tolist()
    window_index = window_starts.index(window_start)
    total_matches = 0

    for np_id in np_columns:
        window_detections = region[np_id].tolist()

        if (window_detections[window_index]):
            total_matches += 1
        
    return total_matches / total_nps



def get_cosegregation(region: pd.DataFrame, window_start_a, window_start_b):
    known_non_np_columns = ['chrom', 'start', 'stop', 'compaction', 'compaction_rating']
    np_columns = [col for col in region.columns if col not in known_non_np_columns]

    total_nps = len(np_columns)
    window_starts: List[int] = region['start'].tolist()
    window_a_index = window_starts.index(window_start_a)
    window_b_index = window_starts.index(window_start_b)
    total_matches = 0

    for np_id in np_columns:
        window_detections = region[np_id].tolist()

        if (window_detections[window_a_index] and window_detections[window_b_index]):
            total_matches += 1
        
    return total_matches / total_nps

def calculate_normalized_linkage(df_a, df_b, df_ab) -> float:
    linkage = calculate_linkage(df_a, df_b, df_ab)

    if linkage < 0:
        return min(df_a * df_b, (1 - df_a) * (1 - df_b))
    else:
        return min(df_b * (1 - df_a), df_a * (1 - df_b))

def calculate_linkage(df_a, df_b, df_ab) -> float:
    return df_ab - df_a * df_b
