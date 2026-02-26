import pandas as pd
from typing import List

# This should probably be more general, but it works for now
def extract_hist1_region(df: pd.DataFrame) -> pd.DataFrame:
    # Just grab the data from chromosome 13
    chr13_df = df[df['chrom'] == 'chr13'].copy()
    
    # Filter for the windows in the hist 1 region
    hist1_df = chr13_df[(chr13_df['start'] <= 24100000) & (chr13_df['stop'] >= 21700000)].copy()
    
    return hist1_df


# Takes our dataframe of just hist1 data and returns just the NPs that
# have at least one genomic window match
def extract_relevant_nps(hist1_df: pd.DataFrame) -> List[str]:
    # Get NP columns
    known_non_np_columns = ['chrom', 'start', 'stop', 'compaction', 'compaction_rating']
    np_columns = [col for col in hist1_df.columns if col not in known_non_np_columns]
    
    # Find NPs that have at least one genomic window match
    relevant_nps = []
    for np_id in np_columns:
        if hist1_df[np_id].any():  # At least one True value
            relevant_nps.append(np_id)
    
    return relevant_nps