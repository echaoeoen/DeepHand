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
