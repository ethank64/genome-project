from statistics import mean
from typing import Dict, List
from models import NPWithDistance
from jaccard_utils import compute_normalized_jaccard_distance
from utils import random_subset


def cluster_data(cluster_count: int, relevant_nps: List[str], region, max_iterations: int) -> Dict[str, List[NPWithDistance]]:
    print("Clustering data...")

    medoids = random_subset(relevant_nps, cluster_count)
    clusters: Dict[str, List[NPWithDistance]] = {}

    for i in range(max_iterations):
        # List is populated with a dict containing np id and distance
        clusters = {np_id: [] for np_id in medoids}

        for relevant_np in relevant_nps:
            # Max 3 keys (for each medoid), scoped to a single relevant NP
            distances = {medoid_id: 0 for medoid_id in medoids}

            # Calculate normalized distances to each cluster medoid
            for medoid_np in medoids:
                # Get genomic window data
                np_data = region[relevant_np].tolist()
                medoid_np_data = region[medoid_np].tolist()

                distance = compute_normalized_jaccard_distance(np_data, medoid_np_data)
                distances[medoid_np] = distance
            
            # Find the minimum distance
            minimum_distance = min(distances.values())

            # Get the np id associated with the minimum distance
            closest_cluster_np = min(distances, key=distances.get)

            # Add the relevant NP with its distance to its assigned cluster
            np_with_dist = NPWithDistance(np_id=relevant_np, distance=minimum_distance)
            clusters[closest_cluster_np].append(np_with_dist)
            
        new_medoids: List[str] = []

        # Find the new best medoids
        for medoid in clusters.keys():
            best_medoid = find_new_best_medoid(medoid, clusters[medoid], region)
            new_medoids.append(best_medoid)
        
        # Checks if the medoids are the same (order doesn't matter)
        if set(new_medoids) == set(medoids):
            print("Medoids are the same after ", i, " iterations")
            break

        medoids = new_medoids

    return clusters



def find_new_best_medoid(current_medoid: str, cluster_nps: List[NPWithDistance], region):
    min_avg_distance = float("inf")
    best_medoid = current_medoid

    for np in cluster_nps:
        distances: List[float] = []

        # Find all of the J distances from the current to every other
        for other_np in cluster_nps:
            if np.np_id != other_np.np_id:
                np_data = region[np.np_id].tolist()
                other_np_data = region[other_np.np_id].tolist()
                distance = compute_normalized_jaccard_distance(np_data, other_np_data)
                distances.append(distance)
        
        avg_distance = mean(distances)

        if avg_distance < min_avg_distance:
            min_avg_distance = avg_distance
            best_medoid = np.np_id

    return best_medoid


def asses_cluster_quality(cluster_data: Dict[str, List[NPWithDistance]]) -> float:
    distances = []

    for medoid in cluster_data.keys():
        nps_with_distance: List[NPWithDistance] = cluster_data[medoid]

        for np in nps_with_distance:
            distances.append(np.distance)

    return mean(distances)


