import serial
import time
import  csv
import requests
class Hand():
	"""docstring for Hand"""
	def __init__(self):
		self.tests=""
		# self.conn = http.client.HTTPSConnection("localhost",port=3000)
	def sendCommand(self,cmd):
		# print(requests)
		r=requests.get( "http://localhost:3000/cmd/"+cmd)
	def grasp(self):
		self.sendCommand("grasp")
	def lateral(self):
		self.sendCommand("lateral")
	def fist(self):
		self.sendCommand("fist")
	def relax(self):
		self.sendCommand("relax")
	def reset(self):
		self.sendCommand("reset")