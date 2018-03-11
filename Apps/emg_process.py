# import neurokit as nk
# processed_emg = nk.emg_process(list_data[0][0:3000])
# Import packages
import neurokit as nk
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import  csv

with open('../Data/female1/cyl_ch1.csv', 'rb') as f:
	reader = csv.reader(f)
	list_data = list(reader)

with open('../Data/female1/cyl_ch2.csv', 'rb') as f:
	reader = csv.reader(f)
	list_data2 = list(reader)

oneCol = list()
for x in xrange(0,len(list_data)):
	oneCol = oneCol + list_data[x]

listnya = [float(x.strip('"')) for x in oneCol]
oneCol = list()
for x in xrange(0,len(list_data2)):
	oneCol = oneCol + list_data2[x]

listnya2 = [float(x.strip('"')) for x in oneCol]

list_data[0] = [float(x.strip('"')) for x in list_data[0]]
processed_emg_ch1 = nk.emg_process(listnya[0:3000])
# df = pd.read_csv("https://raw.githubusercontent.com/neuropsychology/NeuroKit.py/master/examples/Bio/bio_100Hz.csv")
# Plot it
processed_emg_ch2 = nk.emg_process(listnya2[0:3000])

data =  pd.DataFrame(data={"ch1":processed_emg_ch1["df"]["EMG_Envelope"], "ch2":processed_emg_ch2["df"]["EMG_Envelope"]});
# print(data.plot())
axes = data.plot()
# axes = processed_emg["df"].plot()

plt.show()