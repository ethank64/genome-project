from pydantic import BaseModel


class AnalysisResult(BaseModel):
    window_count: int
    np_count: int
    average_windows_per_np: float
    smallest_window_count: int
    largest_window_count: int
    average_nps_per_window: float
    smallest_np_count: int
    largest_np_count: int
