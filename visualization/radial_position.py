import matplotlib.pyplot as plt
from models import NP
import numpy as nump
from typing import List

def plot_radial_position(nuclear_profiles: List[NP]):
    radial_position_ratings = nump.array([np.radial_position_rating for np in nuclear_profiles])

    plt.hist(radial_position_ratings)
    plt.xlabel("Radial Position Rating")
    plt.ylabel("Number of Nuclear Profiles")
    plt.title("Distribution of Nuclear Profile by Radial Position")
    plt.show()