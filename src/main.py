from analysis.linkage import get_normalized_linkage_table
from analysis.network import (
    build_communities,
    fill_in_neo4j,
    get_community_ids,
    get_network_df,
    get_q3_value,
    print_community_stats,
    print_network_stats,
    reset_network,
)
from data_handlers.data_parser import extract_data, extract_features
from data_handlers.subset_extraction import extract_hist1_region

from neo4j import GraphDatabase
from visualization.community_heatmap import plot_community_heatmaps
from visualization.graph_to_json import write_community_graphs_json


def main():
    URI = "neo4j://localhost:7687"
    AUTH = ("neo4j", "Password123*")

    df = extract_data("./data/data.txt")
    feature_df = extract_features("./data/features.csv")
    hist1_df = extract_hist1_region(df)

    linkage_df = get_normalized_linkage_table(hist1_df)

    q3 = get_q3_value(linkage_df)
    print(q3)
    network_df = get_network_df(linkage_df, q3)

    print("Connecting to graph db")
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
        reset_network(driver)
        fill_in_neo4j(driver, network_df)
        # print_network_stats(driver)

        # Get 5 communities
        community_starts = get_community_ids(driver)
        build_communities(driver, community_starts, linkage_df, network_df)
        print_community_stats(driver, feature_df)
        write_community_graphs_json(driver, network_df)
        plot_community_heatmaps(network_df, driver)


if __name__ == "__main__":
    main()

