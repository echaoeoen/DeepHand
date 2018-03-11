import neurokit as nk
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.animation as animation

class Segmentation:
	def __init__(self, raw,signalClass,LABELS):
		self.raw = raw
		self.signalClass = signalClass
		self.LABELS = LABELS

		self.encoded = self.run()

	def run(self):
		process = nk.emg_process(self.raw)
		# self.encoded = process["df"]
		return process["df"]

	def displayPlot(self):
		self.axes = self.encoded.plot()
		plt.title(self.LABELS[self.signalClass])
		plt.show()