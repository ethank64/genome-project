from typing import Dict, List
from models import NP, ClusterSet


def get_cluster_feature_correlations(cluster: List[NP], region_df, features_df) -> Dict[str, float]:
    cluster_feature_correlations = {}

    for np in cluster:
        np_window_data = region_df[np.id].to_list()

        for feature_id, feature_data in features_df.items():
            total_windows = 0
            feature_matches = 0

            for i in range(len(np_window_data)):
                if np_window_data[i]:
                    total_windows += 1

                if np_window_data[i] and np_window_data[i] == feature_data[i]:
                    feature_matches += 1
            
            feature_ratio = feature_matches / total_windows
            cluster_feature_correlations[feature_id] = feature_ratio

    return cluster_feature_correlations


def get_cluster_set_feature_correlations(cluster_set: ClusterSet, region_df, features_df) -> Dict[str, Dict[str, float]]:
    cluster_set_correlations = {}

    clusters = cluster_set.clusters

    for medoid in clusters:
        cluster: List[NP] = clusters[medoid]
        cluster_set_correlations[medoid] = get_cluster_feature_correlations(cluster, region_df, features_df)

    return cluster_set_correlations

        