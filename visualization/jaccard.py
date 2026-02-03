import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import List


def plot_jaccard_heatmap(matrix: List[List[float]], np_labels: List[str], title: str):
    # Convert to numpy array for easier handling
    matrix_array = np.array(matrix)
    
    # Create figure with appropriate size
    fig, ax = plt.subplots(figsize=(14, 12))
    
    # Create heatmap using seaborn
    sns.heatmap(
        matrix_array,
        cmap='viridis',
        vmin=0,
        vmax=1,
        square=True,
        cbar_kws={'label': 'Jaccard Similarity'},
        ax=ax
    )
    
    plt.title(title)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    plt.show()

