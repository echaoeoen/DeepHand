
import tensorflow as tf

# if tf.test.gpu_device_name():
#     print('Default GPU Device: {}'.format(tf.test.gpu_device_name()))
# else:
#     print("Please install GPU version of TF")

import sdautoencoder
sess = tf.Session()
v = sdautoencoder.weight_variable(10,5,"weights")
b = sdautoencoder.bias_variable(5,0,"biases")
sess.run(tf.initialize_all_variables())
weights = sess.run(v)
biases = sess.run(b)
print(weights,biases)