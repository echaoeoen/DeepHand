import csv

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

#!/usr/bin/env python3
 
import time, random
import math
from collections import deque

start = time.time()

class RealtimePlot:
	def __init__(self, axes, axex2, max_entries = 250):
		self.axis_x = deque(maxlen=max_entries)
		self.axis_y = deque(maxlen=max_entries)
		self.axis_x2 = deque(maxlen=max_entries)
		self.axis_y2 = deque(maxlen=max_entries)
		self.axes = axes
		self.axes2 = axes2
		self.max_entries = max_entries
		
		self.lineplot, = axes.plot([], [], "")
		self.lineplot2, = axes2.plot([], [], "")
		self.axes.set_autoscaley_on(True)

	def add(self, x, y,x2,y2):
		# print(x,y)
		self.axis_x.append(x)
		self.axis_y.append(y)
		self.axis_x2.append(x2)
		self.axis_y2.append(y2)
		self.lineplot.set_data(self.axis_x, self.axis_y)
		self.lineplot2.set_data(self.axis_x2, self.axis_y2)

		self.axes.set_xlim(self.axis_x[0], self.axis_x[-1] + 1e-15)
		self.axes.relim(); self.axes.autoscale_view() # rescale the y-axis
		self.axes2.set_xlim(self.axis_x2[0], self.axis_x2[-1] + 1e-15)
		self.axes2.relim(); self.axes2.autoscale_view() # rescale the y-axis

	def animate(self, figure, callback, interval = 50):
		import matplotlib.animation as animation
		def wrapper(frame_index):
			self.add(*callback(frame_index))
			self.axes.relim(); self.axes.autoscale_view() # rescale the y-axis
			return self.lineplot
		animation.FuncAnimation(figure, wrapper, interval=interval)

from matplotlib import pyplot as plt
import matplotlib.animation as animation

# fig, axes = plt.subplots()
# display = RealtimePlot(axes)
# display.animate(fig, lambda frame_index: (time.time() - start, random.random() * 100))
# plt.show()

fig, (axes,axes2) = plt.subplots(2)

display = RealtimePlot(axes,axes2,3000)
y = 0
# for x in xrange(0,len(listnya)):
for x in xrange(0,1000):
	y+= 0.002
	display.add(y, listnya[x],y, listnya2[x])
	if(x % 100 == 0):
		plt.pause(0.002)
plt.show()

# while True:
# 	kiri = time.time() - start
# 	kanan = (random.random() * 100) -100
# 	print(kiri,kanan)
# 	display.add(kiri,kanan)
# 	plt.pause(0.001)

# fig = plt.figure()
# ax1 = fig.add_subplot(1,1,1)

# xar = []
# yar = []
# x=0

# def animate(i):
# 	global x
# 	x+=1
# 	xar.append(time.time() - start)
# 	yar.append(listnya[x])	
# 	ax1.clear()
# 	ax1.plot(xar,yar)
# 	ax1.set_xlim(xar[0], xar[-1] + 1e-15)
# 	ax1.relim(); ax1.autoscale_view() 
# ani = animation.FuncAnimation(fig, animate, interval=1)
# plt.show()

# if __name__ == "__main__": main()