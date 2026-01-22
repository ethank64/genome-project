from data_parser import extract_data
from utils import fill_in_compaction, fill_in_detection_frequency

'''
What we need to find: Detection frequency for all NPs
Detection frequency is the percentage of genomic windows detected by the NP
    - windows/np
    - On a scale from 1-5

Also need the compaction of each genomic window
    - nps/total nps
So we should have a GenomicWindow class
'''


def main():
        nuclear_profiles, genomic_windows = extract_data("./data.txt")

        fill_in_detection_frequency(nuclear_profiles, len(genomic_windows))
        fill_in_compaction(genomic_windows, len(nuclear_profiles))

        # results: AnalysisResult = analyze_data(nuclear_profiles, genomic_windows)

        # show_results(results)

if __name__ == "__main__":
    main()

