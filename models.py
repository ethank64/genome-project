from pydantic import BaseModel
from typing import List

class NP(BaseModel):
    id: str
    windows: List[bool]
    detection_frequency: float = None
    # High DF -> More equatorial
    radial_position_rating: int = None # From 1 (towards the outside) to 5 (towards the center)

class GenomicWindow(BaseModel):
    start: int
    stop: int
    NPs: List[str]   # All the NPs in which that slice was found in
    compaction: float = None
    compaction_rating: int = None # From 1 (spread out) to 10 (compact)


class AnalysisResult(BaseModel):
    window_count: int
    np_count: int
    average_windows_per_np: float
    smallest_window_count: int
    largest_window_count: int
    average_nps_per_window: float
    smallest_np_count: int
    largest_np_count: int
