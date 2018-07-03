import  csv
import pandas as pd
import neurokit as nk
from utils import makeMultiClass
CLASS_CYLINDER = [0,0,0,0,0,0];
CLASS_HOOK = [0,0,0,0,0,1];
CLASS_TIP = [0,0,0,0,1,0];
CLASS_SPHERE = [0,0,0,1,0,0];
CLASS_PALM = [0,0,1,0,0,0];
CLASS_LATERAL = [0,1,0,0,0,0];
LABEL_CLASS=["Cylinder","Hook","Tip","Palm","Lateral"]
LABEL_CLASS_CODE=[CLASS_CYLINDER,CLASS_HOOK,CLASS_TIP,CLASS_PALM,CLASS_LATERAL]

Path = [{"ch1":"../Data/female1/cyl_ch1.csv","ch2":"../Data/female1/cyl_ch2.csv","SignalClass":CLASS_CYLINDER},
{"ch1":"../Data/female1/hook_ch1.csv","ch2":"../Data/female1/hook_ch2.csv","SignalClass":CLASS_HOOK},
{"ch1":"../Data/female1/lat_ch1.csv","ch2":"../Data/female1/lat_ch2.csv","SignalClass":CLASS_LATERAL},
{"ch1":"../Data/female1/palm_ch1.csv","ch2":"../Data/female1/palm_ch2.csv","SignalClass":CLASS_PALM},
{"ch1":"../Data/female1/spher_ch1.csv","ch2":"../Data/female1/spher_ch2.csv","SignalClass":CLASS_SPHERE},
{"ch1":"../Data/female1/tip_ch1.csv","ch2":"../Data/female1/tip_ch2.csv","SignalClass":CLASS_TIP},
{"ch1":"../Data/female2/cyl_ch1.csv","ch2":"../Data/female2/cyl_ch2.csv","SignalClass":CLASS_CYLINDER},
{"ch1":"../Data/female2/hook_ch1.csv","ch2":"../Data/female2/hook_ch2.csv","SignalClass":CLASS_HOOK},
{"ch1":"../Data/female2/lat_ch1.csv","ch2":"../Data/female2/lat_ch2.csv","SignalClass":CLASS_LATERAL},
{"ch1":"../Data/female2/palm_ch1.csv","ch2":"../Data/female2/palm_ch2.csv","SignalClass":CLASS_PALM},
{"ch1":"../Data/female2/spher_ch1.csv","ch2":"../Data/female2/spher_ch2.csv","SignalClass":CLASS_SPHERE},
{"ch1":"../Data/female2/tip_ch1.csv","ch2":"../Data/female2/tip_ch2.csv","SignalClass":CLASS_TIP},
{"ch1":"../Data/female3/cyl_ch1.csv","ch2":"../Data/female3/cyl_ch2.csv","SignalClass":CLASS_CYLINDER},
{"ch1":"../Data/female3/hook_ch1.csv","ch2":"../Data/female3/hook_ch2.csv","SignalClass":CLASS_HOOK},
{"ch1":"../Data/female3/lat_ch1.csv","ch2":"../Data/female3/lat_ch2.csv","SignalClass":CLASS_LATERAL},
{"ch1":"../Data/female3/palm_ch1.csv","ch2":"../Data/female3/palm_ch2.csv","SignalClass":CLASS_PALM},
{"ch1":"../Data/female3/spher_ch1.csv","ch2":"../Data/female3/spher_ch2.csv","SignalClass":CLASS_SPHERE},
{"ch1":"../Data/female3/tip_ch1.csv","ch2":"../Data/female3/tip_ch2.csv","SignalClass":CLASS_TIP},
{"ch1":"../Data/male1/cyl_ch1.csv","ch2":"../Data/male1/cyl_ch2.csv","SignalClass":CLASS_CYLINDER},
{"ch1":"../Data/male1/hook_ch1.csv","ch2":"../Data/male1/hook_ch2.csv","SignalClass":CLASS_HOOK},
{"ch1":"../Data/male1/lat_ch1.csv","ch2":"../Data/male1/lat_ch2.csv","SignalClass":CLASS_LATERAL},
{"ch1":"../Data/male1/palm_ch1.csv","ch2":"../Data/male1/palm_ch2.csv","SignalClass":CLASS_PALM},
{"ch1":"../Data/male1/spher_ch1.csv","ch2":"../Data/male1/spher_ch2.csv","SignalClass":CLASS_SPHERE},
{"ch1":"../Data/male1/tip_ch1.csv","ch2":"../Data/male1/tip_ch2.csv","SignalClass":CLASS_TIP},
{"ch1":"../Data/male2/cyl_ch1.csv","ch2":"../Data/male2/cyl_ch2.csv","SignalClass":CLASS_CYLINDER},
{"ch1":"../Data/male2/hook_ch1.csv","ch2":"../Data/male2/hook_ch2.csv","SignalClass":CLASS_HOOK},
{"ch1":"../Data/male2/lat_ch1.csv","ch2":"../Data/male2/lat_ch2.csv","SignalClass":CLASS_LATERAL},
{"ch1":"../Data/male2/palm_ch1.csv","ch2":"../Data/male2/palm_ch2.csv","SignalClass":CLASS_PALM},
{"ch1":"../Data/male2/spher_ch1.csv","ch2":"../Data/male2/spher_ch2.csv","SignalClass":CLASS_SPHERE},
{"ch1":"../Data/male2/tip_ch1.csv","ch2":"../Data/male2/tip_ch2.csv","SignalClass":CLASS_TIP}
]

Data = list()
SignalClass = list()
DataTest = list()
SignalClassTest = list()
for x in range(0,len(Path)):
	with open(Path[x]["ch1"], 'r') as f:
		reader = csv.reader(f)
		listCh1 = list(reader)
	with open(Path[x]["ch2"], 'r') as f:
		reader = csv.reader(f)
		listCh2 = list(reader)
	AllData = list()
	TestData = list()
	for n in range(0,len(listCh1)-5):
		listnya = listCh1[n]+listCh2[n]
		listnya = [float(x.strip('"')) for x in listnya]
		# AllData += [listnya]
		emg = nk.emg_process(listnya)
		AllData += [emg["df"]["EMG_Envelope"]]
		SignalClass += [Path[x]["SignalClass"]]
	for n in range(len(listCh1)-5,len(listCh1)):
		listnya = listCh1[n]+listCh2[n]
		listnya = [float(x.strip('"')) for x in listnya]
		# TestData+=[listnya]
		emg = nk.emg_process(listnya)
		TestData += [emg["df"]["EMG_Envelope"]]
		SignalClassTest += [Path[x]["SignalClass"]]
	# AllData = [float(x.strip('"')) for x in AllData]
	Data = Data + AllData
	DataTest = DataTest + TestData
# SignalClass = makeMultiClass(SignalClass)
# SignalClassTest = makeMultiClass(SignalClassTest)
# print(len(Data))
# print(len(SignalClass))
# print(len(DataTest))
# print(len(SignalClassTest))

# Data = [[float(y.strip('"')) for y in x] for x in Data]
# DataTest = [[float(y.strip('"')) for y in x] for x in DataTest]
my_df = pd.DataFrame(Data)
my_df.to_csv('../data/trainX.csv', index=False, header=False)
my_df = pd.DataFrame(SignalClass)
my_df.to_csv('../data/trainY.csv', index=False, header=False)
my_df = pd.DataFrame(DataTest)
my_df.to_csv('../data/testX.csv', index=False, header=False)
my_df = pd.DataFrame(SignalClassTest)
my_df.to_csv('../data/testY.csv', index=False, header=False)
# with open("../data/trainX.csv","w") as csvfile :
# 	spamwriter = csv.writer(csvfile,  delimiter=',',quoting=csv.QUOTE_ALL)
# 	print(Data)
# 	spamwriter.writerows(Data)
# with open("../data/trainY.csv","w") as csvfile :
# 	spamwriter = csv.writer(csvfile,  delimiter=',',quoting=csv.QUOTE_ALL)
# 	spamwriter.writerows(Data)
# with open("../data/testX.csv","w") as csvfile :
# 	spamwriter = csv.writer(csvfile,  delimiter=',',quoting=csv.QUOTE_ALL)
# 	spamwriter.writerows(DataTest)
# with open("../data/testY.csv","w") as csvfile :
# 	spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
# 	spamwriter.writerows(SignalClassTest)