from typing import Dict, List
import string
from pydantic import BaseModel


class NP(BaseModel):
    np_id: str
    distance: float



# Just a group of k clusters
class ClusterSet(BaseModel):
    clusters: Dict[str, List[NP]]
    quality: float