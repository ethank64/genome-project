import pandas as pd
from utils import map_range

def fill_in_compaction(df: pd.DataFrame, min_rating: int, max_rating: int) -> pd.DataFrame:
    known_non_np_columns = ['chrom', 'start', 'stop', 'compaction', 'compaction_rating']
    np_columns = [col for col in df.columns if col not in known_non_np_columns]
    total_nps = len(np_columns)
    
    df['compaction'] = 1 - df[np_columns].sum(axis=1) / total_nps
    
    data_min = 0.853
    data_max = df['compaction'].max()
    
    # Map the actual compaction to a value between our selected range
    df['compaction_rating'] = df['compaction'].apply(
        lambda x: map_range(x, data_min, data_max, min_rating, max_rating)
    )
    
    return df


