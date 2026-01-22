from data_parser import extract_data
from utils import fill_in_compaction, fill_in_radial_position
from visualization.compaction import plot_compaction
from visualization.radial_position import plot_radial_position

def main():
        nuclear_profiles, genomic_windows = extract_data("./data.txt")

        fill_in_radial_position(nuclear_profiles, len(genomic_windows), 1, 5)
        fill_in_compaction(genomic_windows, len(nuclear_profiles), 1, 10)

        plot_radial_position(nuclear_profiles)
        plot_compaction(genomic_windows)
        

        # results: AnalysisResult = analyze_data(nuclear_profiles, genomic_windows)

        # show_results(results)

if __name__ == "__main__":
    main()

