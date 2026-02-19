from statistics import mean
from typing import Dict, List
from analysis.clustering import asses_cluster_quality, cluster_data
from data_parser import extract_data
from subset_extraction import (
    extract_hist1_region,
    extract_relevant_nps,
)
from models import ClusterSet, NPWithDistance
from visualization.clusters import visualize_cluster_heatmaps



def main():
        # Extract data into DataFrame
        df = extract_data("./data.txt")
        
        # Extract Hist1 region
        hist1_df = extract_hist1_region(df)
        relevant_nps: List[str] = extract_relevant_nps(hist1_df)

        CLUSTER_COUNT = 3
        MAX_CLUSTER_ITERATIONS = 100

        cluster_sets: List[ClusterSet] = []

        for _ in range(5):
            clusters: Dict[str, List[NPWithDistance]] = cluster_data(CLUSTER_COUNT, relevant_nps, hist1_df, MAX_CLUSTER_ITERATIONS)
            cluster_quality = asses_cluster_quality(clusters)

            cluster_sets.append(ClusterSet(
                clusters=clusters,
                quality=cluster_quality
            ))

        best_cluster_set = find_best_cluster_set(cluster_sets)

        print(f"Best cluster set quality: {best_cluster_set.quality}")
        print(f"Number of clusters: {len(best_cluster_set.clusters)}")
        
        # Visualize each cluster as a heatmap
        visualize_cluster_heatmaps(best_cluster_set, hist1_df)


def find_best_cluster_set(cluster_sets: List[ClusterSet]):
    best_quality = 1
    best_index = -1

    for i in range(len(cluster_sets)):
        quality = cluster_sets[i].quality

        if quality < best_quality:
            best_quality = quality
            best_index = i
    
    return cluster_sets[best_index]

if __name__ == "__main__":
    main()

