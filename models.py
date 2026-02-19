from typing import Dict, List
import string
from pydantic import BaseModel


class NPWithDistance(BaseModel):
    np_id: str
    distance: float


# Just a group of k clusters
class ClusterSet(BaseModel):
    clusters: Dict[str, List[NPWithDistance]]
    quality: float