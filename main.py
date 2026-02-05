from statistics import mean
from typing import Dict, List
from analysis.clustering import asses_cluster_quality, cluster_data
from data_parser import extract_data
from subset_extraction import (
    extract_hist1_region,
    extract_relevant_nps,
)
from models import NPWithDistance

def main():
        # Extract data into DataFrame
        df = extract_data("./data.txt")
        
        # Extract Hist1 region
        hist1_df = extract_hist1_region(df)
        relevant_nps: List[str] = extract_relevant_nps(hist1_df)

        CLUSTER_COUNT = 3
        MAX_CLUSTER_ITERATIONS = 100

        # Pick 3 random nps for initial clustering
        clusters: Dict[str, List[NPWithDistance]] = cluster_data(CLUSTER_COUNT, relevant_nps, hist1_df, MAX_CLUSTER_ITERATIONS)
        cluster_quality = asses_cluster_quality(clusters)

        cluster_ids = clusters.keys()

        print("NPs used for final clusters:")
        for id in cluster_ids:
            print(id)

        print()
        print("Cluster quality (closer to zero is good): ", cluster_quality)
        
        

if __name__ == "__main__":
    main()

