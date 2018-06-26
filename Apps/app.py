import loadData
import numpy
from modules.Segmentation import Segmentation 
# from modules.autoencoder import DenoisingAutoencoder 
from modules.Classification import *
import modules.utils as utils
import time
import sys

def test_SdA(structure, epochTrain, noiseRate, epochFinalLayer, epochFinetune):
	globalTime = time.time()
	X=numpy.array(loadData.Data)
	
	y =numpy.array(loadData.SignalClass)
	y = utils.makeMultiClass(y)
	# y = numpy.array(loadData.LABEL_CLASS_CODE)
	TestX = numpy.array(loadData.DataTest)
	TestY = numpy.array(loadData.SignalClassTest)
	TestY = utils.makeMultiClass(TestY)

	# building the SDA
	sDA = StackedDA(structure)

	# pre-trainning the SDA
	start = time.time()
	
	sDA.pre_train(X, noise_rate=noiseRate, epochs=epochTrain)

	print("---pretrain time: %s seconds ---" % (time.time() - start))
	
	start = time.time()
	
	sDA.finalLayer(X, y, epochs=epochFinalLayer)
	print("---Adding Final Layer time: %s seconds ---" % (time.time() - start))
	
	start = time.time()
	
	sDA.fine_tune(X, y, epochs=epochFinetune)
	print("---Training time: %s seconds ---" % (time.time() - start))
	
	pred = sDA.predict(TestX).argmax(1)

	# let's see how the network did
	TestY = TestY.argmax(1)
	e = 0.0
	for i in range(len(TestY)):
		e += TestY[i]==pred[i]

	# printing the result, this structure should result in 80% accuracy
	
	print("--- %s seconds ---" % (time.time() - globalTime))
	
	print "accuracy: %2.2f%%"%(100*e/len(y))

	return sDA

if __name__ == "__main__":
	layers = [3000]
	if(len(sys.argv)>1):
		layers = sys.argv[1]
		layers = layers.split(",")
		layers = [int(x.strip('"')) for x in layers]
	epochTrain = 2
	if (len(sys.argv) > 2 ):
		epochTrain = int(sys.argv[2])
	noiseRate = 0.0001
	if(len(sys.argv)>3):
		noiseRate = float(sys.argv[3])
	epochFinalLayer = 2
	if(len(sys.argv)>4):
		epochFinalLayer = int(sys.argv[4])
	epochFinetune = 2
	if(len(sys.argv)>5):
		epochFinetune = int(sys.argv[5])
	test_SdA(layers,epochTrain,noiseRate,epochFinalLayer,epochFinetune)