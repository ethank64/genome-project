from typing import List

def create_jaccard_similarity_matrix(df, relevant_nps) -> List[List[float]]:
    print("Creating Jaccard matrix")
    
    matrix = []

    for i in range(len(relevant_nps)):
        column = []

        # This can be optimized, but this is easier
        # to work with for now
        for j in range(len(relevant_nps)):
            np_data_1 = df[relevant_nps[i]].tolist()
            np_data_2 = df[relevant_nps[j]].tolist()
            j_index = compute_jaccard_index(np_data_1, np_data_2)
            column.append(j_index)
        matrix.append(column)
    
    return matrix

def create_jaccard_distance_matrix(df, relevant_nps) -> List[List[float]]:
    print("Creating Jaccard matrix")
    
    matrix = []

    for i in range(len(relevant_nps)):
        column = []

        # This can be optimized, but this is easier
        # to work with for now
        for j in range(len(relevant_nps)):
            np_data_1 = df[relevant_nps[i]].tolist()
            np_data_2 = df[relevant_nps[j]].tolist()
            j_index = compute_jaccard_distance(np_data_1, np_data_2)
            column.append(j_index)
        matrix.append(column)
    
    return matrix

def compute_jaccard_index(np_data_1, np_data_2) -> float:
    # Where genomic window is both 1 in the same spot
    matches = 0

    # M11 + M01 + M10
    denominator = 0

    # Lists are parallel
    for i in range(len(np_data_1)):
        if np_data_1[i] and np_data_2[i]:
            matches += 1
            denominator += 1
        elif not np_data_1[i] and np_data_2[i]:
            denominator += 1
        elif np_data_1[i] and not np_data_2[i]:
            denominator += 1
    
    return matches / denominator

def compute_jaccard_distance(np_data_1, np_data_2) -> float:
    # Where genomic window is both 1 in the same spot
    matches = 0

    # M11 + M01 + M10
    denominator = 0

    # Lists are parallel
    for i in range(len(np_data_1)):
        if np_data_1[i] and np_data_2[i]:
            matches += 1
            denominator += 1
        elif not np_data_1[i] and np_data_2[i]:
            denominator += 1
        elif np_data_1[i] and not np_data_2[i]:
            denominator += 1
    
    return 1 - (matches / denominator)