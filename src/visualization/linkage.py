import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from constants import GRAPHS_DIR


def plot_linkage_heatmap(df: pd.DataFrame):
    numeric_df = df.astype(float)
    n = len(numeric_df)
    fig_size = max(10, n * 0.2)
    fig, ax = plt.subplots(figsize=(fig_size, fig_size))
    sns.heatmap(numeric_df, ax=ax, cbar_kws={"label": "Normalized linkage"})
    ax.set_title("Normalized linkage table - Hist1 region")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    save_path = GRAPHS_DIR / "linkage_heatmap.png"
    GRAPHS_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path, bbox_inches="tight", dpi=300)