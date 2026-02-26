from statistics import mean
from typing import Dict, List
from models import NP
from .jaccard import compute_normalized_jaccard_distance
from utils import random_subset
from models import ClusterSet


def iterate_clusters(relevant_nps, region, cluster_set_count, max_iterations = 100, cluster_size = 3) -> List[ClusterSet]:
    cluster_sets: List[ClusterSet] = []

    for _ in range(10):
        clusters: Dict[str, List[NP]] = cluster_data(cluster_size, relevant_nps, region, max_iterations)
        cluster_quality = asses_cluster_quality(clusters)

        cluster_sets.append(ClusterSet(
            clusters=clusters,
            quality=cluster_quality
        ))

    return cluster_sets


def cluster_data(cluster_count: int, relevant_nps: List[str], region, max_iterations: int) -> Dict[str, List[NP]]:
    medoids = random_subset(relevant_nps, cluster_count)
    clusters: Dict[str, List[NP]] = {}

    for i in range(max_iterations):
        # List is populated with a dict containing np id and distance
        clusters = {np_id: [] for np_id in medoids}

        # For all relevant NPs, find the distances between all the medoids
        for relevant_np in relevant_nps:
            distances = {medoid_id: 0 for medoid_id in medoids}

            # Get normalized distances to each medoid
            for medoid_np in medoids:
                # Get genomic window data
                np_data = region[relevant_np].tolist()
                medoid_np_data = region[medoid_np].tolist()

                distance = compute_normalized_jaccard_distance(np_data, medoid_np_data)
                distances[medoid_np] = distance
            
            # Find the minimum distance
            minimum_distance = min(distances.values())

            # Compare values & return key (np id)
            closest_cluster_np = min(distances, key=distances.get)

            # Add the relevant NP with its distance to its assigned cluster
            np_with_dist = NP(id=relevant_np, distance=minimum_distance)
            clusters[closest_cluster_np].append(np_with_dist)
            
        # Find the new best medoids
        new_medoids: List[str] = []

        # For each old medoid...
        for medoid in clusters.keys():
            best_medoid = find_new_best_medoid(medoid, clusters[medoid], region)
            new_medoids.append(best_medoid)
        
        if set(new_medoids) == set(medoids):
            break

        medoids = new_medoids

    return clusters


# FInds the new best medoid by checking all NPs in the cluster to see which one
# yields the lowest average distance
def find_new_best_medoid(current_medoid: str, cluster_nps: List[NP], region):
    # Edge cases
    if len(cluster_nps) == 0:
        return current_medoid
    if len(cluster_nps) == 1:
        return cluster_nps[0].id
    
    min_avg_distance = float("inf")
    best_medoid = current_medoid

    for np in cluster_nps:
        distances: List[float] = []

        # Find all of the J distances from the current to every other
        for other_np in cluster_nps:
            if np.id != other_np.id:
                np_data = region[np.id].tolist()
                other_np_data = region[other_np.id].tolist()
                distance = compute_normalized_jaccard_distance(np_data, other_np_data)
                distances.append(distance)
        
        if len(distances) > 0:
            avg_distance = mean(distances)

            if avg_distance < min_avg_distance:
                min_avg_distance = avg_distance
                best_medoid = np.id

    return best_medoid


# Finds the average of all the distances
def asses_cluster_quality(cluster_data: Dict[str, List[NP]]) -> float:
    distances = []

    for medoid in cluster_data.keys():
        nps_with_distance: List[NP] = cluster_data[medoid]

        for np in nps_with_distance:
            distances.append(np.distance)

    return mean(distances)


def find_best_cluster_set(cluster_sets: List[ClusterSet]):
    best_quality = 1
    best_index = -1

    for i in range(len(cluster_sets)):
        quality = cluster_sets[i].quality

        if quality < best_quality:
            best_quality = quality
            best_index = i
    
    return cluster_sets[best_index]