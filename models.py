from pydantic import BaseModel
from typing import List

class NP(BaseModel):
    id: str
    windows: List[bool]

class GenomicWindow(BaseModel):
    start: int
    stop: int
    NPs: List[str]   # All the NPs in which that slice was found in

class AnalysisResult(BaseModel):
    window_count: int
    np_count: int
    average_windows_per_np: float
    smallest_window_count: int
    largest_window_count: int
    average_nps_per_window: float
    smallest_np_count: int
    largest_np_count: int
