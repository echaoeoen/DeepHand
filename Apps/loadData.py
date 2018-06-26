import  csv

CLASS_CYLINDER = 0;
CLASS_HOOK = 1;
CLASS_TIP = 2;
CLASS_SPHERE = 3;
CLASS_PALM = 4;
CLASS_LATERAL = 5;
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
SignalClass = []
DataTest = list()
SignalClassTest = []
for x in xrange(0,len(Path)):
	with open(Path[x]["ch1"], 'rb') as f:
		reader = csv.reader(f)
		listCh1 = list(reader)
	with open(Path[x]["ch2"], 'rb') as f:
		reader = csv.reader(f)
		listCh2 = list(reader)
	AllData = list()
	TestData = list()
	for n in xrange(0,len(listCh1)-10):
		AllData += [listCh1[n]+listCh2[n]]
		SignalClass.append(Path[x]["SignalClass"])
	for n in xrange(len(listCh1)-10,len(listCh1)):
		TestData += [listCh1[n]+listCh2[n]]
		SignalClassTest.append(Path[x]["SignalClass"])
	# AllData = [float(x.strip('"')) for x in AllData]
	Data = Data + AllData
	DataTest = DataTest + TestData
Data = [[float(y.strip('"')) for y in x] for x in Data]
DataTest = [[float(y.strip('"')) for y in x] for x in DataTest]