import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from Model_3.plot.plot_RS import plot_RS

data02 = pd.read_csv("data/data02.csv")
data = np.zeros([3, 16, 4], dtype=np.float)
for i in range(len(data02)):
    id = int(data02.loc[i]["id"] - 1)
    t = data02.loc[i]["t"]
    cod = data02.loc[i]["COD"]
    rs = data02.loc[i]["RS"]
    p = data02.loc[i]["P"]
    data[id, i % 16, :] = np.array([t, cod, rs, p]).astype(np.float)
plot_RS(data)