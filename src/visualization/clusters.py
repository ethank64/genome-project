import matplotlib.pyplot as plt
import seaborn as sns
from models import ClusterSet
import numpy as np
import pandas as pd


def visualize_cluster_heatmaps(cluster_set: ClusterSet, region_df: pd.DataFrame):
    cluster_set_data = cluster_set.clusters.items()

    for medoid_id, cluster_nps in cluster_set_data:
        np_ids = [np.np_id for np in cluster_nps]
        np_ids_in_cluster = [medoid_id]
        np_ids_in_cluster.extend(np_ids)

        columns = np_ids_in_cluster
        
        cluster_data = region_df[columns].copy()
        
        # switch rows/cols
        cluster_matrix = cluster_data.T
        
        plot_single_cluster_heatmap(
            cluster_matrix.values,
            medoid_id,
            len(cluster_nps) + 1  # +1 for the medoid
        )


def plot_single_cluster_heatmap(matrix: np.ndarray, medoid_id: str, cluster_size: int):
    num_windows = matrix.shape[1]
    num_nps = matrix.shape[0]
    
    fig_width = max(16, num_windows * 0.15)
    fig_height = max(10, num_nps * 0.8)
    
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    
    # Create heatmap using seaborn
    sns.heatmap(
        matrix,
        cmap='RdYlBu_r',
        vmin=0,
        vmax=1,
        cbar_kws={'label': 'Segregation Value'},
        xticklabels=False,
        yticklabels=False,
        ax=ax,
        square=True,
    )
    
    plt.title(f"Cluster with Medoid: {medoid_id} (Size: {cluster_size} NPs, {num_windows} genomic windows)", 
              fontsize=12, pad=15)
    ax.set_xlabel("Genomic Window Data", fontsize=11, labelpad=10)
    ax.set_ylabel("NPs", fontsize=11, labelpad=10)
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.1)
    plt.savefig("medoid_cluster_" + medoid_id, dpi=300)

