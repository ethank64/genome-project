from typing import Dict, List
from analysis.linkage import get_normalized_linkage_table
from data_handlers.data_parser import extract_data
from data_handlers.subset_extraction import (
    extract_hist1_region,
)
from visualization.linkage import plot_linkage_heatmap


def main():
    df = extract_data("./data/data.txt")
    hist1_df = extract_hist1_region(df)

    linkage_df = get_normalized_linkage_table(hist1_df)
    plot_linkage_heatmap(linkage_df)

if __name__ == "__main__":
    main()

