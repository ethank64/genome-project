from pyexpat import features
from statistics import mean
from typing import Dict, List
from analysis.clustering import asses_cluster_quality, cluster_data
from data_parser import extract_data, extract_features
from subset_extraction import (
    extract_hist1_region,
    extract_relevant_nps,
)
from models import ClusterSet, NP
from analysis.clustering import find_best_cluster_set
from utils import fill_in_radial_position
from visualization.features import plot_feature_boxplots


def main():
    df = extract_data("./data/data.txt")
    features_df = extract_features("./data/features.csv")

    hist1_df = extract_hist1_region(df)
    relevant_nps: List[str] = extract_relevant_nps(hist1_df)

    CLUSTER_COUNT = 3
    MAX_CLUSTER_ITERATIONS = 100

    cluster_sets: List[ClusterSet] = []

    for _ in range(1):
        clusters: Dict[str, List[NP]] = cluster_data(CLUSTER_COUNT, relevant_nps, hist1_df, MAX_CLUSTER_ITERATIONS)
        cluster_quality = asses_cluster_quality(clusters)

        cluster_sets.append(ClusterSet(
            clusters=clusters,
            quality=cluster_quality
        ))

    best_cluster_set: ClusterSet = find_best_cluster_set(cluster_sets)

    clusters: Dict[str, List[NP]] = best_cluster_set.clusters

    hist1_feature_data = features_df["Hist1"].to_list()
    lad_feature_data = features_df["LAD"].to_list()

    hist1_feature_ratios: Dict[str, List[float]] = {}
    lad_feature_ratios: Dict[str, List[float]] = {}

    for medoid in clusters:
        cluster: List[NP] = clusters[medoid]

        local_hist1_ratios: List[float] = []
        local_lad_ratios: List[float] = []

        for np in cluster:
            np_window_data = hist1_df[np.np_id].to_list()

            total_windows = 0
            hist1_matches = 0
            lad_matches = 0

            for i in range(len(np_window_data)):
                if np_window_data[i]:
                    total_windows += 1

                if np_window_data[i] and np_window_data[i] == hist1_feature_data[i]:
                    hist1_matches += 1

                if np_window_data[i] and np_window_data[i] == lad_feature_data[i]:
                    lad_matches += 1

            hist1_percentage = hist1_matches / total_windows
            lad_percentage = lad_matches / total_windows

            local_hist1_ratios.append(hist1_percentage)
            local_lad_ratios.append(lad_percentage)
        
        hist1_feature_ratios[medoid] = local_hist1_ratios
        lad_feature_ratios[medoid] = local_lad_ratios

    plot_feature_boxplots(hist1_feature_ratios, lad_feature_ratios)


    radial_position_df = fill_in_radial_position(hist1_df, 1, 5)

    print(radial_position_df)





if __name__ == "__main__":
    main()

