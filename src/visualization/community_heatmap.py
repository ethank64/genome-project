from typing import List, Set, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from neo4j import Driver

from constants import GRAPHS_DIR


def fetch_community_members(driver: Driver) -> List[tuple[int, Set[int]]]:
    query = """
    MATCH (w:Window)
    WHERE w.community_start IS NOT NULL
    RETURN w.community_start AS community_id, collect(w.start) AS members
    """
    communities: List[Tuple[int, Set[int]]] = []

    with driver.session() as session:
        for record in session.run(query):
            cid = record["community_id"]
            members = {int(start) for start in record["members"]}
            communities.append((int(cid), members))
    return communities


def plot_community_heatmaps(network_df: pd.DataFrame, driver: Driver) -> None:
    window_starts = network_df.index.to_list()
    window_count = len(window_starts)

    communities = fetch_community_members(driver)
    GRAPHS_DIR.mkdir(parents=True, exist_ok=True)

    fig_size = max(10, window_count * 0.2)

    for community_id, member_set in communities:
        masked = pd.DataFrame(np.nan, index=network_df.index, columns=network_df.columns, dtype=float)

        for window_a in window_starts:
            for window_b in window_starts:
                if window_a not in member_set or window_b not in member_set:
                    continue

                if int(network_df.loc[window_a, window_b]) == 1:
                    masked.loc[window_a, window_b] = 1.0

        fig, ax = plt.subplots(figsize=(fig_size, fig_size))
        sns.heatmap(
            masked,
            ax=ax,
            cbar_kws={"label": "1 = edge in community"},
        )
        ax.set_title(f"Community {community_id}")
        plt.xticks(rotation=45, ha="right")
        plt.yticks(rotation=0)
        plt.tight_layout()

        save_path = GRAPHS_DIR / f"community_{community_id}_heatmap.png"
        plt.savefig(save_path, bbox_inches="tight", dpi=300)
        plt.close(fig)
