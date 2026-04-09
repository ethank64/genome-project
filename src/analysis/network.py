import json
from math import floor
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd
from neo4j import Driver

def get_q3_value(linkage_table: pd.DataFrame) -> float:
    linkages: List[float] = []

    for window_a in linkage_table.index:
        for window_b in linkage_table.columns:
            linkage = linkage_table.loc[window_a, window_b]
            linkages.append(float(linkage))

    linkages.sort()

    length = len(linkages)
    q3_index = floor(length * 0.75)
    return linkages[q3_index]


def get_network_df(linkage_table, q3_val) -> pd.DataFrame:
    rows = linkage_table.index
    cols = linkage_table.columns
    network_df = pd.DataFrame(index=rows, columns=cols)

    for window_a in network_df.index:
        for window_b in network_df.columns:
            linkage = linkage_table.loc[window_a, window_b]

            if linkage <= q3_val:
                network_df.loc[window_a, window_b] = 0
                continue

            network_df.loc[window_a, window_b] = 1

    return network_df

def fill_in_neo4j(driver: Driver, network_df: pd.DataFrame):
    window_starts = network_df.index.to_list()

    edges: List[Dict[str, int]] = []
    for i, window_a in enumerate(window_starts):
        # Iterate over the upper triangular matrix
        for window_b in window_starts[i + 1 :]:
            if network_df.loc[window_a, window_b] != 1:
                continue

            edges.append({"window_a": int(window_a), "window_b": int(window_b)})

    with driver.session() as session:
        session.run(
            """
            UNWIND $ids AS window_start
            MERGE (:Window {start: window_start})
            """,
            ids=window_starts,
        )

        session.run(
            """
            UNWIND $edges AS e
            MATCH (a:Window {start: e.window_a}), (b:Window {start: e.window_b})
            MERGE (a)-[:LINKED]->(b)
            """,
            edges=edges,
        )

    write_window_graph_to_json(window_starts, edges)
    

def write_window_graph_to_json(window_starts, edges: List[Dict[str, int]]):
    out = Path(__file__).resolve().parent.parent.parent / "data" / "graph_data.json"

    data = {
        "nodes": [{"id": int(start)} for start in window_starts],
        "links": [{"source": edge["window_a"], "target": edge["window_b"]} for edge in edges],
    }

    out.write_text(json.dumps(data), encoding="utf-8")


def reset_network(driver: Driver) -> None:
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")


def print_network_stats(driver: Driver) -> None:
    get_degrees_query = """
    MATCH (w:Window)
    OPTIONAL MATCH (w)-[r:LINKED]-()
    RETURN w.start AS start, count(r) AS degree
    ORDER BY degree ASC, start ASC
    """

    ranked_windows: List[Tuple[int, int]] = []

    with driver.session() as session:
        for record in session.run(get_degrees_query):
            window_with_rank = (record["start"], int(record["degree"]))
            ranked_windows.append(window_with_rank)

    degrees: List[int] = []
    for _, d in ranked_windows:
        degrees.append(d)

    average_degree_centrality = sum(degrees) / len(degrees)
    min_degree_centrality = min(degrees)
    max_degree_centrality = max(degrees)

    print(f"Average degree centrality: {average_degree_centrality}")
    print(f"Min degree centrality: {min_degree_centrality}")
    print(f"Max degree centrality: {max_degree_centrality}")
    print("Genomic windows ranked by degree centrality:")

    for start, centrality in ranked_windows:
        print(f"Start: {start}, Centrality: {centrality}")

