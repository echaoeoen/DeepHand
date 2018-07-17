import  csv
import pandas as pd
import neurokit as nk
import numpy as np
from utils import makeMultiClass
DataTrain = list()
ClassTrain = list()
DataTest = list()
ClassTest = list()
with open("../../Apps/Data.csv","r") as f:
	reader = csv.reader(f)
	Train = list(reader)
	for x in (range(0,len(Train))):
		Train[x] =[float(n.strip('"')) for n in Train[x]]
		Train[x][len(Train[x])-1] = int(Train[x][len(Train[x])-1])
		ClassTrain += [Train[x][len(Train[x])-1]]
		del(Train[x][len(Train[x])-1])
		emg = nk.emg_process(Train[x])
		DataTrain += [emg["df"]["EMG_Envelope"]]

with open("../../Apps/test.csv","r") as f:
	reader = csv.reader(f)
	Test = list(reader)
	for x in (range(0,len(Test))):
		Test[x] =[float(n.strip('"')) for n in Test[x]]
		Test[x][len(Test[x])-1] = int(Test[x][len(Test[x])-1])

		ClassTest += [Test[x][len(Test[x])-1]]
		del(Test[x][len(Test[x])-1])
		emg = nk.emg_process(Test[x])
		DataTest += [emg["df"]["EMG_Envelope"]]
ClassTest = makeMultiClass(ClassTest)
ClassTrain = makeMultiClass(ClassTrain)

print(ClassTrain[0])

my_df = pd.DataFrame(DataTrain)
my_df.to_csv('../data/trainX.csv', index=False, header=False)
my_df = pd.DataFrame(ClassTrain)
my_df.to_csv('../data/trainY.csv', index=False, header=False)
my_df = pd.DataFrame(DataTest)
my_df.to_csv('../data/testX.csv', index=False, header=False)
my_df = pd.DataFrame(ClassTest)
my_df.to_csv('../data/testY.csv', index=False, header=False)
