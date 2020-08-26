import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
def plot_COD_RS(data, a, b, rr):
    print(a, b, rr)
    cod = data[:, 1]
    rs = data[:, 2]
    X = np.arange(0, 50, 1)
    Y = a * X + b

    fig, ax = plt.subplots()  # 建立了慕布
    for key, spine in ax.spines.items():
        if key == "right" or key == "top":
            spine.set_visible(False)
        if key == "left" or key == "bottom":
            spine.set_linewidth(2)
    ax.tick_params(width=2, length=7)
    plt.xlabel("Rs Concentration(g/L)", {"family": "DejaVu", "size": 22, "weight": "normal"})
    plt.ylabel("COD Concentration(g/L)", {"family": "DejaVu", "size": 22, "weight": "normal"})
    plt.tick_params(labelsize=16)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    plt.xlim([0, 50])
    plt.ylim([0, 90])
    for label in labels:
        label.set_fontname("DejaVu")

    colors = ["black", "#4c51b4ff", "tomato"]
    markers = ["s", "o", "v"]
    plt.scatter(rs, cod, color="w", edgecolors=colors[2], marker=markers[1], linewidth=2, label="Raw Data")
    plt.plot(X, Y, color="black", label="Fitted", linewidth=2)
    plt.text(3, 40 * a + b, "y = %.3f x + %.3f" % (a, b), fontsize=16)
    plt.text(3, 40 * a + b - 10, "${R^2=%.3f}$" % rr, fontsize=16)

    # plt.legend(fontsize=16)
    plt.show()

def plot_RS(data):
    t = data[0, :, 0]
    rs = data[:, :, 2]

    fig, ax = plt.subplots()  # 建立了慕布
    for key, spine in ax.spines.items():
        if key == "right" or key == "top":
            spine.set_visible(False)
        if key == "left" or key == "bottom":
            spine.set_linewidth(2)
    ax.tick_params(width=2, length=7)
    plt.xlabel("Time / hour", {"family": "DejaVu", "size":22, "weight": "normal"})
    plt.ylabel("Rs Concentration / g/L", {"family": "DejaVu", "size": 22, "weight": "normal"})
    plt.tick_params(labelsize=16)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    plt.xlim([0, 100])
    plt.ylim([0, 50])
    for label in labels:
        label.set_fontname("DejaVu")
    colors = ["black", "#4c51b4ff", "tomato", "red"]
    # markers = ["s", "o", "v"]
    for i in range(4):
        print("%.3f g/L" % rs[i, 0])
        plt.plot(t, rs[i, :], linewidth=2, label="%.3f g/L" % rs[i, 0])
    plt.legend(fontsize=16)
    plt.show()

def plot_v(x, y, flag):
    data = y[flag]
    print(data.shape)

    fig, ax = plt.subplots()  # 建立了慕布
    for key, spine in ax.spines.items():
        if key == "right" or key == "top":
            spine.set_visible(False)
        if key == "left" or key == "bottom":
            spine.set_linewidth(2)
    ax.tick_params(width=2, length=7)
    plt.xlabel("Time(hour))", {"family": "DejaVu", "size": 22, "weight": "normal"})
    plt.ylabel("Concentration(g/L)", {"family": "DejaVu", "size": 22, "weight": "normal"})
    plt.tick_params(labelsize=16)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    plt.xlim([0, 100])
    plt.ylim([-5, 7])
    for label in labels:
        label.set_fontname("DejaVu")
    colors = ["black", "#4c51b4ff", "tomato"]
    markers = ["s", "o", "v"]
    labels = ["COD", "RS", "P"]
    for i in range(3):
        print("%.3f g/L" % data[i, 0])
        plt.plot(x, data[:, i + 1], color=colors[i], linewidth=2, label=labels[i])
    plt.legend(fontsize=16)
    plt.show()

def plot_fit_v(x, y, fit_y):

    fig, ax = plt.subplots()  # 建立了慕布
    for key, spine in ax.spines.items():
        if key == "right" or key == "top":
            spine.set_visible(False)
        if key == "left" or key == "bottom":
            spine.set_linewidth(2)
    ax.tick_params(width=2, length=7)
    plt.xlabel("Time(hour))", {"family": "DejaVu", "size": 22, "weight": "normal"})
    plt.ylabel("Concentration(g/L)", {"family": "DejaVu", "size": 22, "weight": "normal"})
    plt.tick_params(labelsize=16)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    plt.xlim([0, 100])
    plt.ylim([-10, 10])
    for label in labels:
        label.set_fontname("DejaVu")
    colors = ["black", "#4c51b4ff", "tomato"]
    markers = ["s", "o", "v"]
    labels = ["COD", "RS", "P"]
    plt.plot(x, y, color=colors[0], linewidth=2, label="Raw Data")
    plt.plot(x, fit_y, color=colors[1], linewidth=2, label="Fitted Data")
    plt.legend(fontsize=16)
    plt.show()

def plot_fitted(x, y, fit_y):

    fig, ax = plt.subplots()  # 建立了慕布
    for key, spine in ax.spines.items():
        if key == "right" or key == "top":
            spine.set_visible(False)
        if key == "left" or key == "bottom":
            spine.set_linewidth(2)
    ax.tick_params(width=2, length=7)
    plt.xlabel("Time(hour))", {"family": "DejaVu", "size": 22, "weight": "normal"})
    plt.ylabel("Concentration(g/L)", {"family": "DejaVu", "size": 22, "weight": "normal"})
    plt.tick_params(labelsize=16)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    plt.xlim([0, 100])
    plt.ylim([0, 100])
    for label in labels:
        label.set_fontname("DejaVu")
    colors = ["black", "#4c51b4ff", "tomato"]
    markers = ["s", "o", "v"]
    labels = ["COD", "RS", "P"]
    plt.plot(x, y, color=colors[0], linewidth=2, label="Raw Data")
    plt.plot(x, fit_y, color=colors[1], linewidth=2, label="Fitted Data")
    plt.legend(fontsize=16)
    plt.show()

def plot_diff_sig(ys, lab):

    fig, ax = plt.subplots()  # 建立了慕布
    for key, spine in ax.spines.items():
        if key == "right" or key == "top":
            spine.set_visible(False)
        if key == "left" or key == "bottom":
            spine.set_linewidth(2)
    ax.tick_params(width=2, length=7)
    plt.xlabel("Time(hour))", {"family": "DejaVu", "size": 22, "weight": "normal"})
    plt.ylabel("P Concentration(g/L)", {"family": "DejaVu", "size": 22, "weight": "normal"})
    plt.tick_params(labelsize=16)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    plt.xlim([0, 100])
    plt.ylim([0, 100])
    for label in labels:
        label.set_fontname("DejaVu")
    # colors = ["black", "#4c51b4ff", "tomato"]
    # markers = ["s", "o", "v"]
    # labels = ["COD", "RS", "P"]
    for i in range(len(ys)):
        plt.plot(np.arange(0, 100), ys[i], linewidth=2, label="dC:" + str(lab[i]))
    plt.legend(fontsize=16)
    plt.show()

