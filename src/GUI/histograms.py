import matplotlib.pyplot as plt
import numpy as np


def draw_histogram(data: list[float], bins: int, title: str = "Histogram", x_label: str = "X-axis",
                   y_label: str = "Y-axis") -> None:
    """
    Draws a histogram from provided data
    :param data: data to draw on histogram
    :param bins: number of bins
    :param title: title of the histogram
    :param x_label: x-axis label
    :param y_label: y-axis label
    """

    plt.hist(data, bins=bins, color="blue", edgecolor="black", alpha=0.7)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
