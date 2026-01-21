from pydantic import BaseModel
from typing import List

class NP(BaseModel):
    id: str
    windows: List[bool]

class AnalysisResult(BaseModel):
    averageWindowsPerNP: float
    smallestWindowCount: int
    largestWindowCount: int

