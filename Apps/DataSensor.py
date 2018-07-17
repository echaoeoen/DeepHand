import serial
import time
import  csv
ser = serial.Serial('/dev/cu.usbmodem1411', 9600, timeout=0.050)
th1 = 0.85
th2 = 0.7
count = 80
t=0
rec =False
ch1=[]
ch2=[]
Y=4

print(":test")
def save(CH1,CH2,Y):
	print(len(CH1))
	data=ch1+ch2+[Y]

	with open("Data.csv","a") as f:
		spamwriter = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		spamwriter.writerow(data)
while True:
	while ser.in_waiting:  # Or: while ser.inWaiting():
		data =ser.readline().decode("utf-8").replace("\r\n","")
		data = data.split(", ")
		data[0] = float(data[0])
		data[1] = float(data[1])
		# print(data)
		if((th1<data[0] or th2 < data[1]) and rec==False ):
			rec = True
			startTime = int(round(time.time() * 1000))
		if(rec):
			t+=1
			ch1+=[data[0]]
			ch2+=[data[1]]
			# if(t == count):
			# if(th1>data[0] or th2 > data[1] ):
			now = int(round(time.time() * 1000))
			# print(now,startTime)
			if(t==count):
				rec=False
				t=0
				save(ch1,ch2,Y)
				print("sleep")
				exit()
				# time.sleep(3)
				print("start")
				ch1=[]
				ch2=[]


