from typing import Dict, List
from pydantic import BaseModel


class NP(BaseModel):
    id: str
    distance: float

# Just a group of k clusters
class ClusterSet(BaseModel):
    clusters: Dict[str, List[NP]]
    quality: float