from data_parser import extract_data
from utils import fill_in_compaction, fill_in_radial_position
from visualization.compaction import plot_compaction
from visualization.radial_position import plot_radial_position
from hist1_analysis import (
    extract_hist1_region,
    analyze_hist1_statistics,
    analyze_hist1_radial_positions,
    analyze_hist1_compactions
)

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
        
        # Hist1 Region Analysis
        print("\n" + "=" * 68)
        print("SINGLE-CELL ANALYSIS OF THE 3D TOPOLOGIES OF GENOMIC LOCI")
        print("Hist1 Region Analysis (Chromosome 13: 21.7 Mb - 24.1 Mb)")
        print("=" * 68)
        
        # Extract Hist1 region
        hist1_df = extract_hist1_region(df)
        
        # Analyze basic statistics
        analyze_hist1_statistics(hist1_df)
        
        # Analyze radial positions (np_info_df already has radial positions calculated)
        analyze_hist1_radial_positions(np_info_df, hist1_df)
        
        # Analyze compactions (hist1_df already has compactions since it was extracted from df)
        analyze_hist1_compactions(hist1_df)

if __name__ == "__main__":
    main()

