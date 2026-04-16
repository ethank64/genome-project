import json
from pathlib import Path
from typing import Dict, List

import pandas as pd
from neo4j import Driver

_VISUALIZATION_DIR = Path("/Users/ethanknotts/Desktop/College/dataScience/activity1/src/visualization")


def write_community_graphs_json(driver: Driver, network_df: pd.DataFrame) -> None:
    from analysis.network import get_degree_centrality_by_start

    centrality: Dict[int, float] = get_degree_centrality_by_start(driver)
    
    grab_communities = """
    MATCH (w:Window)
    WHERE w.community_start IS NOT NULL
    RETURN w.community_start AS community_id, collect(w.start) AS members
    ORDER BY community_id
    """

    communities: List[Dict] = []

    with driver.session() as session:
        for record in session.run(grab_communities):
            community_id = record["community_id"]
            member_starts = [int(start) for start in record["members"]]
            hub_id = int(community_id)

            nodes = []

            for start in member_starts:
                node = {}
                node["id"] = start
                node["val"] = float(centrality.get(start, 0.0))

                if start == hub_id:
                    node["color"] = "red"
                else:
                    node["color"] = "yellow"

                nodes.append(node)

            links: List[Dict[str, int]] = []
            for i, window_a in enumerate(member_starts):

                for window_b in member_starts[i + 1 :]:
                    if int(network_df.loc[window_a, window_b]) == 1:
                        links.append({"source": window_a, "target": window_b})

            communities.append(
                {
                    "community_start": int(community_id),
                    "nodes": nodes,
                    "links": links,
                }
            )

    out = _VISUALIZATION_DIR / "community_graphs.json"
    out.write_text(json.dumps({"communities": communities}))
