import loadData
import numpy
from modules.Segmentation import Segmentation 
# from modules.autoencoder import DenoisingAutoencoder 
from modules.Classification import *
import modules.utils as utils
import modules.Sda as DNN
import time
def test_SdA(pretrain_lr=0.1, pretraining_epochs=500, corruption_level=0.3, \
			 finetune_lr=0.1, finetune_epochs=200):
	globalTime = time.time()
	X=numpy.array(loadData.Data)
	y =numpy.array(loadData.SignalClass)
	y = utils.makeMultiClass(y)
	# y = numpy.array(loadData.LABEL_CLASS_CODE)
	
	# building the SDA
	sDA = StackedDA([1000,300,500])

	# pre-trainning the SDA
	start = time.time()
	
	sDA.pre_train(X[:900], noise_rate=0.0001, epochs=2)

	print("---pretrain time: %s seconds ---" % (time.time() - start))
	
	start = time.time()
	
	sDA.finalLayer(X[:900], y[:900], epochs=2)
	print("---Adding Final Layer time: %s seconds ---" % (time.time() - start))
	
	start = time.time()
	
	sDA.fine_tune(X[:900], y[:900], epochs=2)
	print("---Training time: %s seconds ---" % (time.time() - start))
	
	pred = sDA.predict(X).argmax(1)

	# let's see how the network did
	y = y.argmax(1)
	e = 0.0
	for i in range(len(y)):
		e += y[i]==pred[i]

	# printing the result, this structure should result in 80% accuracy
	
	print("--- %s seconds ---" % (time.time() - globalTime))
	
	print "accuracy: %2.2f%%"%(100*e/len(y))

	return sDA
	# da = DenoisingAutoencoder(n_hidden=10)
	# fit = da.fit(numpy.array(loadData.Data))
	# new_X = da.transform(loadData.Data)
	# print(new_X)

	# ListSegmented = list()
	# SegmentedEMG = []
	# for x in xrange(0,len(loadData.Data)):
	# 	S= Segmentation(loadData.Data[x],loadData.SignalClass[x],loadData.LABEL_CLASS)
	# 	SegmentedEMG.append(S.encoded["EMG_Envelope"].as_matrix()) 
	# 	ListSegmented += [S]

	# loadData.SignalClass = numpy.array([[x] for x in loadData.SignalClass])
	# rng = numpy.random.RandomState(123)

	# # construct SdA
	# sda = DNN.SdA(input=numpy.array(SegmentedEMG), label=loadData.SignalClass, \
	#           n_ins=6000, hidden_layer_sizes=[5, 5], n_outs=1, numpy_rng=rng)

	# # pre-training

	# start_time = time.time()

	# print("--- Start Training ")
	
	# sda.pretrain(lr=pretrain_lr, corruption_level=corruption_level, epochs=pretraining_epochs)

	# print("--- training time in %s seconds ---" % (time.time() - start_time))
	# # fine-tuning
	# start_time = time.time()

	# sda.finetune(lr=finetune_lr, epochs=finetune_epochs)
	# print("--- finetuning time in %s seconds ---" % (time.time() - start_time))


	# # test
	# x = SegmentedEMG[0]
	# start_time = time.time()

	# print sda.predict(x)
	# print("--- finetuning time in %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
	test_SdA()

# ListSegmented[0].displayPlot()
# axes = ListSegmented[0].plot();

# print(ListSegmented[0]["EMG_Envelope"])