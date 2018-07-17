from sdautoencoder import SDAutoencoder, get_batch_generator, merge_generators, stopwatch, DEBUG
import tensorflow as tf
import numpy as np
import  csv
import sys
import pickle

# X_TRAIN_PATH = "../data/x_train_transformed_SAM_2.csv"
# Y_TRAIN_PATH = "../data/splits/OPYTrainSAM.csv"
# X_TEST_PATH = "../data/x_test_transformed_SAM_2.csv"
# Y_TEST_PATH = "../data/splits/OPYTestSAM.csv"

# NEED TO RENAME FOR EVERY TRIAL
OUTPUT_PATH = "../data/deephand/pred.csv"
TRANSFORMED_PATH = "../data/deephand/transformed.csv"

X_TRAIN_PATH = "../data/trainX.csv"
Y_TRAIN_PATH = "../data/trainY.csv"
X_TEST_PATH = "../data/testX.csv"
Y_TEST_PATH = "../data/testY.csv"
BIASES_PATH = "../data/biases.csv"
WEIGHT_PATH = "../data/weights.csv"
VARIABLE_SAVE_PATH = "../data/deephand/last_vars.ckpt"


def average(lst):
    return sum(lst) / len(lst)


def append_with_limit(lst, val, limit=10):
    """Non-destructive function that returns a copy of the original list with the appended value and limit."""
    lst_copy = lst[:]
    lst_copy.append(val)
    return lst_copy[-limit:]


def write_data(data, filename):  # FIXME: Copied from sda, should refactor to static
    """Writes data in data_tensor and appends to the end of filename in csv format.

    :param data: A 2-dimensional numpy array.
    :param filename: A string representing the save filepath.
    :return: None
    """
    with open(filename, "ab") as file:
        np.savetxt(file, data, delimiter=",")


@stopwatch
def train_softmax(input_dim, output_dim, x_train_filepath, y_train_filepath, lr=0.001, batch_size=100,
                  print_step=50, epochs=1):
    """Trains a softmax model for prediction."""
    # Model input and parameters
    x = tf.placeholder(tf.float32, [None, input_dim])
    weights = tf.Variable(tf.truncated_normal(shape=[input_dim, output_dim], stddev=0.1))
    biases = tf.Variable(tf.constant(0.1, shape=[output_dim]))

    # Outputs and true y-values
    y_logits = tf.matmul(x, weights) + biases
    y_pred = tf.nn.softmax(y_logits)
    y_actual = tf.placeholder(tf.float32, [None, output_dim])

    # Cross entropy and training step
    cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=y_logits, labels=y_actual))
    train_step = tf.train.AdamOptimizer(learning_rate=lr).minimize(cross_entropy)

    # Start session and run batches based on number of epochs
    sess = tf.Session()
    sess.run(tf.initialize_all_variables())
    x_train = get_batch_generator(filename=x_train_filepath, batch_size=batch_size,
                                  repeat=epochs - 1)

    y_train = get_batch_generator(filename=y_train_filepath, batch_size=batch_size,
                                  repeat=epochs - 1)
    step = 0
    accuracy_history = []
    for batch_xs, batch_ys in zip(x_train, y_train):
        sess.run(train_step, feed_dict={x: batch_xs, y_actual: batch_ys})

        # Debug
        # if step == 100:
        #     break

        # Assess training accuracy for current batch
        if step % print_step == 0:
            correct_prediction = tf.equal(tf.argmax(y_pred, 1), tf.argmax(y_actual, 1))
            accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
            accuracy_val = sess.run(accuracy, feed_dict={x: batch_xs, y_actual: batch_ys})
            print("Step %s, current batch training accuracy: %s" % (step, accuracy_val))
            accuracy_history = append_with_limit(accuracy_history, accuracy_val)

        # Assess training accuracy for last 10 batches
        if step > 0 and step % (print_step * 10) == 0:
            print("Predicted y-values:\n", sess.run(y_pred, feed_dict={x: batch_xs}))
            print("Overall batch training accuracy for steps %s to %s: %s" % (step - 10 * print_step,
                                                                              step,
                                                                              average(accuracy_history)))

        step += 1

    parameters_dict = {
        "weights": sess.run(weights),
        "biases": sess.run(biases)
    }
    sess.close()
    return parameters_dict


@stopwatch
def test_model(parameters_dict, input_dim, output_dim, x_test_filepath, y_test_filepath, output_filepath,
               batch_size=100, print_step=100):
    x_test = get_batch_generator(filename=x_test_filepath, batch_size=batch_size)
    # print("test_x")
    # print(list(x_test))
    y_test = get_batch_generator(filename=y_test_filepath, batch_size=batch_size)  # FIXME: Check if headers
    xy_test_gen = merge_generators(x_test, y_test)
    test_model_gen(parameters_dict, input_dim, output_dim, xy_test_gen, output_filepath, print_step)

def get_class(parameters_dict, input_dim, output_dim, data):
    x = tf.placeholder(tf.float32, [None, input_dim])

    weights = parameters_dict["weights"]
    biases = parameters_dict["biases"]

    # Outputs and true y-values
    y_pred = tf.nn.softmax(tf.matmul(x, weights) + biases)
    y_actual = tf.placeholder(tf.float32, [None, output_dim])

    # Evaluate testing accuracy

    correct_prediction = tf.equal(tf.argmax(y_pred, 1), tf.argmax(y_actual, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    sess = tf.Session()
    c = sess.run(y_pred, feed_dict={x:data})
    return c[0]
@stopwatch
def test_model_gen(parameters_dict, input_dim, output_dim, xy_test_gen, output_filepath, print_step=1):
    """

    :param parameters_dict: Must contain keys 'weights' and 'biases' with their respective values
    :param input_dim:
    :param output_dim:
    :param x_test_filepath:
    :param y_test_filepath:
    :param output_filepath:
    :param batch_size:
    :param print_step:
    :return:
    """
    # Model input and parameters
    x = tf.placeholder(tf.float32, [None, input_dim])

    weights = parameters_dict["weights"]
    biases = parameters_dict["biases"]

    # Outputs and true y-values
    y_pred = tf.nn.softmax(tf.matmul(x, weights) + biases)
    y_actual = tf.placeholder(tf.float32, [None, output_dim])

    # Evaluate testing accuracy

    correct_prediction = tf.equal(tf.argmax(y_pred, 1), tf.argmax(y_actual, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    sess = tf.Session()

    step = 0
    accuracy_history = []
    for batch_xs, batch_ys in xy_test_gen:
        # print(batch_xs)
        data=sess.run(y_pred, feed_dict={x: batch_xs})
        write_data(data, filename=output_filepath)
        print(data)
        pred =[]
        sc = []
        for i in range(0,len(data[0])):
            sc.append(0.0)
        for i in range(0,len(data)):
            choise = 0
            maxInd = -1
            tm = sc[:]
            for j in range(0,len(data[i])):
                # print(maxInd,data[i][j],maxInd < data[i][j])
                if(maxInd < data[i][j]):
                    maxInd = data[i][j]
                    choise = j
            tm[choise] = 1.0
            pred.append(tm)
        b=0
        batch_ys = [[float(y.strip('"')) for y in x] for x in batch_ys]
        
        print(pred)
        print(batch_ys)
        for i in range(0,len(pred)):
            print(pred[i],batch_ys[i],pred[i]==batch_ys[i])
            if(pred[i]==batch_ys[i]):
                b+=1
        print(len(pred),b)
        accuracy_val = b/len(pred)

        # Break early if debug
        if DEBUG and step == 10:
            break

        accuracy_val = sess.run(accuracy, feed_dict={x: batch_xs, y_actual: batch_ys})
        # print(accuracy_val)
        accuracy_history.append(accuracy_val)

        # if step % print_step == 0:
        #     print("Step %s, current batch testing accuracy: %s" % (step, accuracy_val))
        #     print("Predicted y-values:\n", sess.run(y_pred, feed_dict={x: batch_xs}))

        step += 1

    sess.close()
    print(accuracy_history)
    print("Testing complete and written to %s, overall accuracy: %s" % (output_filepath, average(accuracy_history)))


@stopwatch
def unsupervised():
    sess = tf.Session()
    sda = SDAutoencoder(dims=[6000, 1000, 500, 200],
                        activations=["sigmoid", "sigmoid", "sigmoid"],
                        sess=sess,
                        noise=0.05,
                        loss="rmse",
                        batch_size=100,
                        print_step=50)

    layer_1_weights_path = "../data/outputs/last_weights"
    layer_1_biases_path = "../data/outputs/last_biases"

    sda.pretrain_network(X_TRAIN_PATH, epochs=8)
    sda.write_data(sda.hidden_layers[1].weights, layer_1_weights_path)
    sda.write_data(sda.hidden_layers[1].biases, layer_1_biases_path)
    sda.write_encoded_input(TRANSFORMED_PATH, X_TEST_PATH)
    sda.save_variables(VARIABLE_SAVE_PATH)
    sess.close()
def clearCsv(filepath):
    f = open(filepath,'w+')
    f.close()

def openData(filepath):
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        d = list(reader)
        d = [[np.float32(n.strip('"'))for n in m] for m in d]
        return np.asarray(d)
@stopwatch
def full_test():
    clearCsv(TRANSFORMED_PATH)
    clearCsv(OUTPUT_PATH)
    clearCsv(BIASES_PATH)
    clearCsv(WEIGHT_PATH)
    # config = tf.ConfigProto()
    # config.gpu_options.allow_growth = True
    sess = tf.Session()
    sda = SDAutoencoder(dims=[160, 80, 30,5],
                        activations=["sigmoid","sigmoid","sigmoid"],
                        sess=sess,
                        noise=0.2,
                        loss="rmse",
                        pretrain_lr=1e-4,
                        finetune_lr=1e-2,
                        batch_size=20,
                        print_step=100)

    sda.pretrain_network(X_TRAIN_PATH, epochs=2000)
    trained_parameters = sda.finetune_parameters(X_TRAIN_PATH, Y_TRAIN_PATH, output_dim=3, epochs=1000)
    sda.write_data(trained_parameters["weights"],WEIGHT_PATH)
    sda.write_data([trained_parameters["biases"]],BIASES_PATH)
    sda.write_encoded_input(TRANSFORMED_PATH, X_TEST_PATH)
    sda.save_variables(VARIABLE_SAVE_PATH)
    sess.close()
    # print(len(sda.hidden_layers))
    # print(sda.hidden_layers[0].weights,sda.hidden_layers[0].biases)
    # print(sda.hidden_layers[1].weights,sda.hidden_layers[1].biases) 

    # with open("sda.file", "wb") as f:
    #     pickle.dump(sda, f, pickle.HIGHEST_PROTOCOL)

    test_model(parameters_dict=trained_parameters,
               input_dim=sda.output_dim,
               output_dim=3,
               x_test_filepath=TRANSFORMED_PATH,
               y_test_filepath=Y_TEST_PATH,
               output_filepath=OUTPUT_PATH)
@stopwatch
def test():
    weight = openData(WEIGHT_PATH)
    biases = openData(BIASES_PATH)
    trained_parameters = {"weights":weight,"biases":biases}
    test_model(parameters_dict=trained_parameters,
               input_dim=5,
               output_dim=3,
               x_test_filepath=TRANSFORMED_PATH,
               y_test_filepath=Y_TEST_PATH,
               output_filepath=OUTPUT_PATH)

def wrap_sensor(X=[]):
    sess = tf.Session()
    # Restore variables from disk.
    new_saver = tf.train.import_meta_graph(VARIABLE_SAVE_PATH+".meta")
    saver = tf.train.Saver()

    saver.restore(sess, tf.train.latest_checkpoint('../data/deephand/'))
    weight = openData(WEIGHT_PATH)
    biases = openData(BIASES_PATH)

    #write encoded
    sda = SDAutoencoder(dims=[160, 80, 30,5],
                    activations=["sigmoid","sigmoid","sigmoid"],
                    sess=sess,
                    noise=0.2,
                    loss="rmse",
                    pretrain_lr=1e-5,
                    finetune_lr=1e-3,
                    batch_size=1,
                    print_step=1)
    print(len(sda.hidden_layers))
    var = tf.all_variables()
    encW = []
    encB = []
    for v in var:
        # print(v.name)
        # print(sess.run(v))
        # if(v.name[0:13]=="hidden_layer_" and v.name[] =="encoding_vars")
        n = v.name.split("/")
        if(len(n)==3):
            if(n[1][0:13]=="hidden_layer_" and n[0] == "finetuning"):
                ind = int(n[1][13:15])
                val = sess.run(v)
                if(n[2]=="weights:0"):
                    sda.hidden_layers[ind].set_weights(val)
                else:
                    sda.hidden_layers[ind].set_biases(val)
    trained_parameters = {"weights":weight,"biases":biases}
    if(len(X)==0):
        X = openData("../data/TestX.csv")
        X = X[14]

    print(type(X),X)
    Transformed = sda.transformX(X)
    print(Transformed)
    c = get_class(parameters_dict=trained_parameters,input_dim=5,output_dim=3,data=[Transformed])
    print(c)
    cS = []
    from HandCommand import Hand
    hand = Hand()
        
    for x in range(len(c)):
        if(c[x]>0.49999): 
            cS.append(1)
        else : 
            cS.append(0)
    if(cS[0]==1):
        hand.lateral()
    elif(cS[1]==1):
        hand.fist()
    elif(cS[2]==1):
        hand.grasp()

    # print(sda.hidden_layers[0].weights)
    # clearCsv("../data/rt.csv")
    # clearCsv("../data/result.csv")
    # # clearCsv(TRANSFORMED_PATH)
    # # clearCsv(OUTPUT_PATH)
    # sda.write_encoded_input("../data/rt.csv", "../data/realTest.csv")

    # sess.close()
    # # print(sda.hidden_layers[0].weights,sda.hidden_layers[0].biases)
    # # print(sda.hidden_layers[1].weights,sda.hidden_layers[1].biases) 
    # # sda.write_encoded_input(TRANSFORMED_PATH, X_TEST_PATH)
    # test_model(parameters_dict=trained_parameters,
    #        input_dim=5,
    #        output_dim=3,
    #        x_test_filepath="../data/rt.csv",
    #        y_test_filepath=Y_TEST_PATH,
    #        output_filepath="../data/result.csv")



    
# @stopwatch
def main():

    func = sys.argv[1]
    print(func)
    if(func =="train"):
        full_test()
    elif(func=="test"):
        print("testing")
        test()
    elif(func=="sensors_test"):
        wrap_sensor()
    else:
        print("Not implemented")
        from HandCommand import Hand
        import time
        hand = Hand()
        # time.sleep(1)
        # hand.reset()
        time.sleep(1)
        hand.lateral()
        time.sleep(5)
        hand.relax()
        time.sleep(5)
        hand.fist()
        time.sleep(5)
        hand.relax()
        time.sleep(5)
        hand.grasp()
        time.sleep(5)
        hand.relax()


if __name__ == "__main__":
    main()