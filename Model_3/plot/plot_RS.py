import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_RS(data):
    t = data[0, :, 0]
    rs = data[:, :, 2]
    fig, ax = plt.subplots()
    for key, spine in ax.spines.items():
        if key == "right" or key == "top":
            spine.set_visible(False)
        if key == "left" or key == "bottom":
            spine.set_linewidth(2)
    ax.tick_params(width=2, length=7)
    plt.xlabel("Time", {"family": "DejaVu", "size":22, "weight": "normal"})
    plt.ylabel("Rs Concentration", {"family": "DejaVu", "size": 22, "weight": "normal"})
    plt.tick_params(labelsize=16)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    plt.xlim([0, 100])
    plt.ylim([0, 50])
    for label in labels:
        label.set_fontname("DejaVu")
    colors = ["black", "#4c51b4ff", "tomato"]
    markers = ["s", "o", "v"]
    for i in range(3):
        print("%.3f g/L" % rs[i, 0])
        plt.plot(t, rs[i, :], color=colors[i], marker=markers[i], linewidth=2, label="%.3f g/L" % rs[i, 0])
    plt.legend(fontsize=16)
    plt.show()