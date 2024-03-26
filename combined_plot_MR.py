import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()

df20 = pd.read_excel("20umspeedvsfreqdata.xlsx")
df5 = pd.read_excel("5umspeedvsfreqdata.xlsx")
df5dimer = pd.read_excel("5umdimerspeedvsfreqdata.xlsx")
df20dimer = pd.read_excel("20umdimerspeedvsfreqdata.xlsx")

mydfs = [df5, df20, df5dimer, df20dimer]
colorset = ["red",  "blue", "green", "black"]
labels = ["5 um: ", "20 um: ", "5 um Dimer: ","20 um Dimer: "]


for (col, df, l) in zip(colorset, mydfs, labels):
    row_freq = df.iloc[:,0]
    row_means = df.iloc[:, 1:].mean(axis=1)
    row_std = df.iloc[:, 1:].std(axis=1)

    coefficients = np.polyfit(row_freq, row_means, 1)
    p = np.poly1d(coefficients)
    equation = f'v = {coefficients[0]:.2f}f + {coefficients[1]:.2f}'
    plot_label = l + equation
    plt.errorbar(row_freq, row_means, yerr = row_std, color = col, fmt='-o', capsize = 5, label = plot_label)
    #plt.plot(row_freq, p(row_freq), color = "k")

ax.set_xlabel("Frequency")
ax.set_ylabel("Velocity (um/s)")


ax.legend()
ax.set_title("Silica Microspheres Coated in 100 nm Nickel \n Speed vs Rotating Magnetic Field Frequency")
plt.show()

