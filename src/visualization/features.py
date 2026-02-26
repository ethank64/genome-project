import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import Dict, List
import numpy as np
from utils import plot_radar, boxplot

from constants import GRAPHS_DIR


def plot_feature_radar(cluster_set_feature_correlations: Dict[str, Dict[str, float]]):
    for medoid in cluster_set_feature_correlations:
        cluster_feature_correlations: Dict[str, float] = cluster_set_feature_correlations[medoid]

        feature_labels = list(cluster_feature_correlations.keys())
        ratios = list(cluster_feature_correlations.values())

        title = "Feature Ratios for " + medoid + " Cluster"
        file_name = "feature_ratios_" + medoid
        save_path = GRAPHS_DIR / file_name

        plot_radar(feature_labels, ratios, title, save_path)


def plot_feature_boxplot(cluster_set_ratios: Dict[str, List[float]], feature_id: str):
    medoids = list(cluster_set_ratios.keys())

    rows = []
    for i, medoid in enumerate(medoids):
        label = f"Cluster {i + 1} ({medoid})"

        for percentage in cluster_set_ratios[medoid]:
            rows.append({"cluster": label, "percentage": percentage * 100})

    feature_df = pd.DataFrame(rows)
    
    x_title = "Cluster"
    y_title = f"Percentage of windows that contain {feature_id}"
    save_path = GRAPHS_DIR / f"boxplot_{feature_id}_feature.png"
    boxplot(feature_df, x_title, y_title, "cluster", "percentage", save_path)

