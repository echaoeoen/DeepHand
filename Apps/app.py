import loadData
import numpy
from modules.Segmentation import Segmentation 
import modules.Sda as DNN
import time
def test_SdA(pretrain_lr=0.1, pretraining_epochs=500, corruption_level=0.3, \
             finetune_lr=0.1, finetune_epochs=200):
	
	ListSegmented = list()
	SegmentedEMG = []
	for x in xrange(0,len(loadData.Data)):
		S= Segmentation(loadData.Data[x],loadData.SignalClass[x],loadData.LABEL_CLASS)
		SegmentedEMG.append(S.encoded["EMG_Envelope"].as_matrix()) 
		ListSegmented += [S]

	loadData.SignalClass = numpy.array([[x] for x in loadData.SignalClass])
	rng = numpy.random.RandomState(123)

	# construct SdA
	sda = DNN.SdA(input=numpy.array(SegmentedEMG), label=loadData.SignalClass, \
	          n_ins=6000, hidden_layer_sizes=[5, 5], n_outs=1, numpy_rng=rng)

	# pre-training

	start_time = time.time()


	sda.pretrain(lr=pretrain_lr, corruption_level=corruption_level, epochs=pretraining_epochs)

	print("--- training time in %s seconds ---" % (time.time() - start_time))
	# fine-tuning
	start_time = time.time()

	sda.finetune(lr=finetune_lr, epochs=finetune_epochs)
	print("--- finetuning time in %s seconds ---" % (time.time() - start_time))


	# test
	x = SegmentedEMG[0]
	start_time = time.time()

	print sda.predict(x)
	print("--- finetuning time in %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    test_SdA()

# ListSegmented[0].displayPlot()
# axes = ListSegmented[0].plot();

# print(ListSegmented[0]["EMG_Envelope"])