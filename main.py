from data_parser import extract_data
from jaccard_utils import compute_normalized_jaccard_distance
from subset_extraction import (
    extract_hist1_region,
    extract_relevant_nps,
)
from typing import List
from utils import random_subset

def main():
        # Extract data into DataFrame
        df = extract_data("./data.txt")
        
        # Extract Hist1 region
        hist1_df = extract_hist1_region(df)
        relevant_nps: List[str] = extract_relevant_nps(hist1_df)

        # similarity_matrix = create_jaccard_similarity_matrix(hist1_df, relevant_nps)
        # distance_matrix = create_jaccard_distance_matrix(hist1_df, relevant_nps)

        # plot_jaccard_heatmap(similarity_matrix, relevant_nps, "Jaccard Similarity Heatmap")
        # plot_jaccard_heatmap(distance_matrix, relevant_nps, "Jaccard Distance Heatmap")

        # Pick 3 random nps for initial clustering
        initial_clusters = random_subset(relevant_nps, 3)
        
        clusters = {np_id: [] for np_id in initial_clusters}

        while True:
            for relevant_np in relevant_nps:
                distances = []

                # Calculate normalized distance
                for cluster_np in initial_clusters:
                    np_data = hist1_df[relevant_np].tolist()
                    cluster_np_data = hist1_df[cluster_np].tolist()
                    distance = compute_normalized_jaccard_distance(np_data, cluster_np_data)
                    distances.append(distance)
                
                minimum_distance = min(distances)
                cluster_index = distances.index(minimum_distance)
                clusters[initial_clusters[cluster_index]].append(relevant_np)
            



if __name__ == "__main__":
    main()

