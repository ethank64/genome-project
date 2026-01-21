from data_parser import extract_data
from models import AnalysisResult
from utils import analyze_data, show_results

'''
What we need to find: Detection frequency for all NPs
Detection frequency is the percentage of genomic windows detected by the NP
    - windows/np
    - On a scale from 1-5

Also need the compaction of each genomic window
    - nps/window

So we should have a GenomicWindow class
'''


def main():
        nuclear_profiles, genomic_windows = extract_data("./data.txt")

        results: AnalysisResult = analyze_data(nuclear_profiles, genomic_windows)

        show_results(results)

if __name__ == "__main__":
    main()

