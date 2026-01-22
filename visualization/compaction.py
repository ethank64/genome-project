import matplotlib.pyplot as plt
from models import GenomicWindow
import numpy as nump

def plot_compaction(genomic_windows: GenomicWindow):
    # Convert compaction data to Numpy array so we can plot it
    compaction_ratings = nump.array([window.compaction_rating for window in genomic_windows])

    plt.hist(compaction_ratings)
    plt.xlabel("Compaction")
    plt.ylabel("Number of Windows")
    plt.title("Distribution of Genomic Window Compaction Values")
    plt.show()