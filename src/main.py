from typing import Dict, List
from analysis import radial_position
from analysis.clustering import iterate_clusters
from data_handlers.data_parser import extract_data, extract_features
from data_handlers.subset_extraction import (
    extract_hist1_region,
    extract_relevant_nps,
)
from models import ClusterSet, NP
from analysis.clustering import find_best_cluster_set
from analysis.radial_position import fill_in_radial_position
from analysis.features import extract_feature_ratios, get_cluster_set_feature_correlations
from visualization.features import plot_feature_boxplot, plot_feature_radar
from visualization.radial_position import plot_cluster_radial_positions



def main():
    df = extract_data("./data/data.txt")
    features_df = extract_features("./data/features.csv")

    hist1_df = extract_hist1_region(df)
    relevant_nps: List[str] = extract_relevant_nps(hist1_df)

    cluster_sets: List[ClusterSet] = iterate_clusters(relevant_nps, hist1_df, 10)
    best_cluster_set: ClusterSet = find_best_cluster_set(cluster_sets)

    feature_correlations: Dict[str, Dict[str, float]] = get_cluster_set_feature_correlations(best_cluster_set, hist1_df, features_df)

    hist1_gene_data: Dict[str: List[float]] = extract_feature_ratios(best_cluster_set, hist1_df, features_df, "Hist1")

    
    plot_feature_radar(feature_correlations)
    plot_feature_boxplot(hist1_gene_data, "Hist1")
    plot_feature_boxplot(hist1_gene_data, "LAD")
    plot_cluster_radial_positions(best_cluster_set, hist1_df)


if __name__ == "__main__":
    main()

