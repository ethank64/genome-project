import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import Dict, List
import numpy as np

from constants import GRAPHS_DIR


def plot_feature_radar(cluster_set_feature_correlations: Dict[str, Dict[str, float]]):
    for medoid in cluster_set_feature_correlations:
        cluster_feature_correlations: Dict[str, float] = cluster_set_feature_correlations[medoid]

        feature_labels = list(cluster_feature_correlations.keys())
        ratios = list(cluster_feature_correlations.values())

        angles = np.linspace(0, 2 * np.pi, len(feature_labels), endpoint=False).tolist()

        angles_closed = angles + angles[:1]
        ratios_closed = ratios + ratios[:1]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

        ax.plot(angles_closed, ratios_closed, linewidth=2)
        ax.fill(angles_closed, ratios_closed, alpha=0.25)

        ax.set_xticks(angles)
        ax.set_xticklabels(feature_labels)

        ax.set_title("Feature Ratios for " + medoid + " Cluster")
        ax.set_ylim(0, 1)

        file_name = "feature_ratios_" + medoid
        plt.savefig(GRAPHS_DIR / file_name, dpi=300)


def plot_feature_boxplots(hist1_ratios: Dict[str, List[float]], lad_ratios: Dict[str, List[float]]):
    medoids = list(hist1_ratios.keys())

    hist1_rows = []
    for i, medoid in enumerate(medoids):
        label = f"Cluster {i + 1} ({medoid})"

        for percentage in hist1_ratios[medoid]:
            hist1_rows.append({"cluster": label, "percentage": percentage * 100})

    hist1_df = pd.DataFrame(hist1_rows)

    lad_rows = []
    for i, medoid in enumerate(medoids):
        label = f"Cluster {i + 1} ({medoid})"

        for percentage in lad_ratios[medoid]:
            lad_rows.append({"cluster": label, "percentage": percentage * 100})

    lad_df = pd.DataFrame(lad_rows)

    fig1, ax1 = plt.subplots(figsize=(6, 5))
    sns.boxplot(data=hist1_df, x="cluster", y="percentage", ax=ax1)
    sns.stripplot(data=hist1_df, x="cluster", y="percentage", color="black", size=3, ax=ax1)
    ax1.set_xlabel("Cluster")
    ax1.set_ylabel("Percentage of windows in an NP that contain histone genes")
    GRAPHS_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(GRAPHS_DIR / "boxplot_hist1_feature.png", dpi=300)

    fig2, ax2 = plt.subplots(figsize=(6, 5))
    sns.boxplot(data=lad_df, x="cluster", y="percentage", ax=ax2)
    sns.stripplot(data=lad_df, x="cluster", y="percentage", color="black", size=3, ax=ax2)
    ax2.set_xlabel("Cluster")
    ax2.set_ylabel("Percentage of windows in an NP that contain LADs")
    plt.savefig(GRAPHS_DIR / "boxplot_lad_feature.png", dpi=300)
