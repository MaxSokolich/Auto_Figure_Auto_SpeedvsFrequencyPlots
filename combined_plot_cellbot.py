import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()

bot1CB = pd.read_excel("1botcellbot_total.xlsx")
bot2CB = pd.read_excel("2botcellbot_total.xlsx")
bot3CB = pd.read_excel("3botcellbot_total.xlsx")
bot4CB = pd.read_excel("4botcellbot_total.xlsx")
bot5CB = pd.read_excel("5botcellbot_total.xlsx")
bot6CB = pd.read_excel("6botcellbot_total.xlsx")



mydfs = [bot1CB, bot2CB, bot3CB,bot4CB]#, bot5CB,bot6CB]
colorset = ["red",  "blue", "green", "orange", "black", "yellow"]
labels = ["1 Bot Cellbot: ", "2 Bot Cellbot: ", "3 Bot Cellbot: ", "4 Bot Cellbot: ", "5 Bot Cellbot: ", "6 Bot Cellbot: "]


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
#ax.set_ylim([0,200])
ax.legend()
ax.set_title("Various Sized Cellbots \n Speed vs Rotating Magnetic Field Frequency")
plt.show()

