import matplotlib.pyplot as plt


def draw_histogram(x: list[float], y: list[float], title: str = "Histogram", x_label: str = "X-axis",
                   y_label: str = "Y-axis") -> None:
    """
    Draws a histogram from provided data
    :param x: x-axis values
    :param y: y-axis values
    :param title: title of the histogram
    :param x_label: x-axis label
    :param y_label: y-axis label
    """
    plt.bar(x, y, width=0.7, color='purple', edgecolor='black')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()