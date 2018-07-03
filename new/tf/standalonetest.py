from softmax import test_model,openData


OUTPUT_PATH = "../data/deephand/pred.csv"
TRANSFORMED_PATH = "../data/deephand/transformed.csv"

X_TRAIN_PATH = "../data/trainX.csv"
Y_TRAIN_PATH = "../data/trainY.csv"
X_TEST_PATH = "../data/testX.csv"
Y_TEST_PATH = "../data/testY.csv"
BIASES_PATH = "../data/biases.csv"
WEIGHT_PATH = "../data/weights.csv"

biases = openData(BIASES_PATH)
# print(type(biases[0][0]))
biases = [[float(y.strip('"')) for y in x] for x in biases]
weights = openData(WEIGHT_PATH)
print(type(weights[0][0]))
weights = [[float(y.strip('"')) for y in x] for x in weights]
trained_parameters = {'biases':biases,'weights':weights}
test_model(parameters_dict=trained_parameters, input_dim=len(weights), output_dim=6, x_test_filepath=TRANSFORMED_PATH, y_test_filepath=Y_TEST_PATH, output_filepath=OUTPUT_PATH)
