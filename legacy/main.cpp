#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <climits>

using namespace std;

struct NP {
    string id;
    vector<bool> windows;
};

struct AnalysisResult {
    double averageWindowsPerNP;
    int smallestWindowCount;
    int largestWindowCount;
};

// Implement Python's awesome split function
vector<string> split(string line, char splitChar);

// Creates vector of NPs with just their IDs
vector<NP> initNPs(vector<string> npIds);

// We use a single function because it's more efficient
// Otherwise, we'd have to iterate over the large dataset multiple times
AnalysisResult analyzeNuclearProfiles(vector<NP> npData);

int main() {
    ifstream data("./data.txt");

    if (!data) {
        cout << "Uh oh, data couldn't be loaded!!" << endl;
        exit(1);
    }

    cout << "Initializing nuclear profiles..." << endl;

    // Get just the first line (has NPs)
    string firstLine;
    getline(data, firstLine);

    // Get all the NP ids
    vector<string> npIds = split(firstLine, '	');
    npIds.erase(npIds.begin(), npIds.begin() + 3);     // Remove the first 3 (not NPs)

    // Initilize master NP vector with IDs
    vector<NP> nuclearProfiles = initNPs(npIds);

    cout << "Parsing genomic window data..." << endl;

    double totalWindowDetections = 0;
    int smallestWindowDetectionCount = INT_MAX;
    int largestWindowDetectionCount = INT_MIN;

    // Parse genomic window data
    string genomicWindow;
    int genomicWindowCount = 0;

    while (getline(data, genomicWindow)) {
        // Get a vector of the window data for that row
        vector<string> windowData = split(genomicWindow, '	');
        windowData.erase(windowData.begin(), windowData.begin() + 3);   // Ignore position info

        int localWindowDetections = 0;  // # of windows detected for the current NP

        // Update all of our NPs with genomic data
        for (int i = 0; i < windowData.size(); i++) {
            string result = windowData.at(i);

            // Update respective NP with window data from that row
            if (result == "0") {
                nuclearProfiles.at(i).windows.push_back(false);
            } else if (result == "1") {
                nuclearProfiles.at(i).windows.push_back(true);
                localWindowDetections++;
            }
        }

        if (localWindowDetections < smallestWindowDetectionCount) {
            smallestWindowDetectionCount = localWindowDetections;
        }
        if (localWindowDetections > largestWindowDetectionCount) {
            largestWindowDetectionCount = localWindowDetections;
        }

        totalWindowDetections += localWindowDetections;

        genomicWindowCount++;   // Each row is a genomic window
    }

    cout << "Analyzing data..." << endl;
    AnalysisResult result = analyzeNuclearProfiles(nuclearProfiles);

    cout << endl << "====================================================================" << endl;
    cout << "Genomic Windows: " << genomicWindowCount << endl;
    cout << "Nuclear Profiles: " << nuclearProfiles.size() << endl;
    cout << "Average windows per NP: " << result.averageWindowsPerNP << endl;
    cout << "Smallest # of windows in any NP: " << result.smallestWindowCount << endl;
    cout << "Largest # of windows in any NP: " << result.largestWindowCount << endl;
    cout << "Average NPs in which a window was detected: " << totalWindowDetections / genomicWindowCount << endl;
    cout << "Smallest # of NPs in which a window was detected: " << smallestWindowDetectionCount << endl;
    cout << "Largest # of NPs in which a window was detected: " << largestWindowDetectionCount << endl;
    cout << "====================================================================" << endl;

    exit(0);
}

vector<string> split(string line, char splitChar) {
    vector<string> splitUpVector;

    // Turn the string into a stream
    stringstream stream(line);
    string token;

    // Get each word, split by the splitChar
    while (getline(stream, token, splitChar)) {
        splitUpVector.push_back(token);
    }
    
    return splitUpVector;
}

vector<NP> initNPs(vector<string> npIds) {
    vector<NP> initWithIds;

    for (int i = 0; i < npIds.size(); i++) {
        NP np;
        np.id = npIds.at(i);

        initWithIds.push_back(np);
    }

    return initWithIds;
}

AnalysisResult analyzeNuclearProfiles(vector<NP> npData) {
    AnalysisResult result;

    double totalNPs = npData.size();
    double totalWindows = 0;
    int smallestNumWindows = INT_MAX;
    int largestNumWindows = INT_MIN;

    for (NP np : npData) {
        int localWindowCount = 0;   // Tracks the number of window for that np

        // Count the number of windows
        for (bool window : np.windows) {
            if (window) localWindowCount++;
        }

        if (localWindowCount < smallestNumWindows) {
            smallestNumWindows = localWindowCount;
        }
        if (localWindowCount > largestNumWindows) {
            largestNumWindows = localWindowCount;
        }

        totalWindows += localWindowCount;
    }

    result.averageWindowsPerNP = totalWindows / totalNPs;
    result.smallestWindowCount = smallestNumWindows;
    result.largestWindowCount = largestNumWindows;

    return result;
}