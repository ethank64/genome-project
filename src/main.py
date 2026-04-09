from analysis.linkage import get_normalized_linkage_table
from analysis.network import (
    fill_in_neo4j,
    get_network_df,
    get_q3_value,
    print_network_stats,
    reset_network,
)
from data_handlers.data_parser import extract_data
from data_handlers.subset_extraction import extract_hist1_region

from neo4j import GraphDatabase


def main():
    URI = "neo4j://localhost:7687"
    AUTH = ("neo4j", "Password123*")

    df = extract_data("./data/data.txt")
    hist1_df = extract_hist1_region(df)

    linkage_df = get_normalized_linkage_table(hist1_df)

    # linage dataframe is literally just the graph! each i j pair is a relationship
    q3 = get_q3_value(linkage_df)
    network_df = get_network_df(linkage_df, q3)

    print("Connecting to graph db")
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
        reset_network(driver)
        fill_in_neo4j(driver, network_df)
        print_network_stats(driver)
    



if __name__ == "__main__":
    main()

