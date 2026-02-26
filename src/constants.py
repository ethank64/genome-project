from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
GRAPHS_DIR = PROJECT_ROOT / "graphs"
FEATURES = ["Hist1", "Vmn", "LAD", "RNAPII-S2P", "RNAPII-S5P", "RNAPII-S7P", "Enhancer", "H3K9me3", "H3K20me3", "h3k27me3", "H3K36me3", "NANOG", "pou5f1", "sox2", "CTCF-7BWU"]
