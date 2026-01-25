from data_parser import extract_data
from utils import fill_in_compaction, fill_in_radial_position
from visualization.compaction import plot_compaction
from visualization.radial_position import plot_radial_position

def main():
        # Extract data into DataFrame
        df = extract_data("./data.txt")

        # Calculate radial position ratings for each NP
        np_info_df = fill_in_radial_position(df, 1, 5)
        
        # Calculate compaction ratings for each window (modifies df in place)
        df = fill_in_compaction(df, 1, 10)

        # Plot visualizations
        plot_radial_position(np_info_df)
        plot_compaction(df)
        

        # results: AnalysisResult = analyze_data(nuclear_profiles, genomic_windows)

        # show_results(results)

if __name__ == "__main__":
    main()

