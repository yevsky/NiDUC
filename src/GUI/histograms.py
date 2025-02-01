import matplotlib.pyplot as plt

def draw_histogram(data: list[float], bins: int, title: str = "Histogram", x_label: str = "X-axis",
                   y_label: str = "Y-axis", color: str = "blue") -> None:
    """
    Draws a histogram from provided data
    :param data: a data to draw on histogram
    :param bins: number of bins
    :param title: title of the histogram
    :param x_label: x-axis label
    :param y_label: y-axis label
    :param color: color of the histogram bins
    """

    plt.hist(data, bins=bins, color=color, edgecolor="black", alpha=0.7)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def draw_sla_histogram(sla_names: list[str], values: list[float], title: str = "SLA Histogram", x_label: str = "SLA Standards",
                       y_label: str = "Values", color: str = "blue") -> None:
    """
    Draws a histogram for SLA standards
    :param sla_names: list of SLA standard names
    :param values: values corresponding to each SLA standard
    :param title: title of the histogram
    :param x_label: x-axis label
    :param y_label: y-axis label
    :param color: color of the histogram bars
    """
    plt.bar(sla_names, values, color=color, edgecolor="black", alpha=0.7)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()