from data_parser import extract_data
from utils import fill_in_compaction, fill_in_radial_position
from subset_extraction import (
    extract_hist1_region,
    extract_relevant_nps,
)
from typing import List
from jaccard_utils import create_jaccard_similarity_matrix, create_jaccard_distance_matrix
from visualization.jaccard import plot_jaccard_heatmap

def main():
        # Extract data into DataFrame
        df = extract_data("./data.txt")

        # Calculate radial position ratings for each NP
        np_info_df = fill_in_radial_position(df, 1, 5)
        
        # Calculate compaction ratings for each window (modifies df in place)
        df = fill_in_compaction(df, 1, 10)

        # Plot visualizations
        # plot_radial_position(np_info_df)
        # plot_compaction(df)
        
        # Extract Hist1 region
        hist1_df = extract_hist1_region(df)
        relevant_nps: List[str] = extract_relevant_nps(hist1_df)

        similarity_matrix = create_jaccard_similarity_matrix(hist1_df, relevant_nps)
        distance_matrix = create_jaccard_distance_matrix(hist1_df, relevant_nps)

        plot_jaccard_heatmap(similarity_matrix, relevant_nps, "Jaccard Similarity Heatmap")
        plot_jaccard_heatmap(distance_matrix, relevant_nps, "Jaccard Distance Heatmap")




if __name__ == "__main__":
    main()

