import json
from math import floor
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd
from neo4j import Driver


def get_degree_centrality_by_start(driver: Driver) -> Dict[int, float]:
    grab_nodes_with_degree = """
    MATCH (w:Window)
    OPTIONAL MATCH (w)-[r:LINKED]-()
    RETURN w.start AS start, count(r) AS degree
    """

    with driver.session() as session:
        nodes = list(session.run(grab_nodes_with_degree))

    node_count = len(nodes)
    if node_count <= 1:
        return {int(node["start"]): 0.0 for node in nodes}

    denom = float(node_count - 1)

    centralities: Dict[int, float] = {}

    for node in nodes:
        start = int(node["start"])
        degree = int(node["degree"])
        centralities[start] = degree / denom

    return centralities

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

    window_count = len(ranked_windows)
    degrees: List[int] = []
    for _, d in ranked_windows:
        degrees.append(d)

    degrees = [degree / (window_count - 1) for degree in degrees]

    average_degree_centrality = sum(degrees) / len(degrees)
    min_degree_centrality = min(degrees)
    max_degree_centrality = max(degrees)

    print(f"Average degree centrality: {average_degree_centrality}")
    print(f"Min degree centrality: {min_degree_centrality}")
    print(f"Max degree centrality: {max_degree_centrality}")
    print("Genomic windows ranked by degree centrality:")

    for start, centrality in ranked_windows:
        print(f"Start: {start}, Centrality: {centrality / (window_count - 1)}")


def get_community_ids(driver: Driver):
    with driver.session() as session:
        result = session.run("""
        MATCH (w:Window)
        OPTIONAL MATCH (w)-[r:LINKED]-()
        RETURN w.start AS start, count(r) AS degree
        ORDER BY degree DESC, start ASC
        LIMIT 5
        """)

        community_ids = []
        for record in result:
            community_ids.append(record["start"])

        return community_ids

def build_communities(driver: Driver, community_starts, linkage_df: pd.DataFrame, network_df: pd.DataFrame):
    community_starts = [int(start) for start in community_starts]

    with driver.session() as session:
        result = session.run("""
        MATCH (w:Window)
        RETURN w.start AS start
        """)

        for node in result:
            current_start = int(node["start"])

            if current_start in community_starts:
                assigned_community = current_start
            else:
                neighboring_hubs = []
                for community_start in community_starts:
                    if int(network_df.loc[current_start, community_start]) == 1:
                        neighboring_hubs.append(community_start)

                if not neighboring_hubs:
                    assigned_community = None
                elif len(neighboring_hubs) == 1:
                    assigned_community = int(neighboring_hubs[0])
                else:
                    best_hub = int(neighboring_hubs[0])
                    highest_linkage = float(linkage_df.loc[current_start, best_hub])

                    for hub in neighboring_hubs[1:]:
                        linkage = float(linkage_df.loc[current_start, int(hub)])
                        if linkage > highest_linkage:
                            highest_linkage = linkage
                            best_hub = int(hub)

                    assigned_community = best_hub

            session.run(
                """
                MATCH (w:Window {start: $current_start})
                SET w.community_start = $assigned_community
                """,
                current_start=current_start,
                assigned_community=assigned_community,
            )


def print_community_stats(driver: Driver, features_df: pd.DataFrame) -> None:
    features_by_start = features_df.set_index("start")

    get_communities = """
    MATCH (w:Window)
    WHERE w.community_start IS NOT NULL
    RETURN w.community_start AS community_id, collect(w.start) AS members
    """

    with driver.session() as session:
        for record in session.run(get_communities):
            community_id = record["community_id"]
            members = [int(start) for start in record["members"]]

            member_count = len(members)
            hist1_positive = 0
            lad_positive = 0

            for window_start in members:
                if window_start not in features_by_start.index:
                    continue

                row = features_by_start.loc[window_start]

                if float(row["Hist1"]) > 0:
                    hist1_positive += 1
                if float(row["LAD"]) > 0:
                    lad_positive += 1

            if not member_count:
                hist1_percentage = 0.0
                lad_percentage = 0.0
            else:
                hist1_percentage = 100.0 * hist1_positive / member_count
                lad_percentage = 100.0 * lad_positive / member_count

            print(f"Community: {community_id}")
            print(f"  Size: {member_count}")
            print(f"  Windows with Hist1 signal: {hist1_percentage}%")
            print(f"  Windows with LAD signal: {lad_percentage}%")
            print(f"  Member window starts: {members}")
            print('\n')