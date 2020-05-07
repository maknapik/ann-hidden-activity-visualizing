import pandas as pd
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Flatten
from keras.optimizers import SGD
from keras.layers import Conv2D, MaxPooling2D
from keras.models import load_model
from network.constants import DataType
from network.constants import MODEL_PATH_PREFIX


def create_multilayer_perceptron(dataType):
    if dataType == DataType.MNIST:
        input_shape = 784
    else:
        input_shape = 3072

    model = Sequential()
    model.add(Dense(1000, activation='relu', input_shape=(input_shape,)))
    model.add(Dropout(0.2))
    model.add(Dense(1000, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(1000, activation='relu'))
    model.add(Dropout(0.4))
    model.add(Dense(1000, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(10, activation='softmax'))

    optimizer = SGD(lr=0.01, momentum=0.9, decay=10e-9)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

    return model


def create_cnn(dataType):
    if dataType == DataType.MNIST:
        input_shape = (28, 28, 1)
        neurons_count = 3136
    else:
        input_shape = (32, 32, 3)
        neurons_count = 4096

    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
    model.add(Conv2D(32, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dropout(0.5))
    model.add(Dense(neurons_count, activation='relu'))
    model.add(Dense(512, activation='relu'))
    model.add(Dense(10, activation='softmax'))

    optimizer = SGD(lr=0.01, momentum=0.9, decay=10e-6)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

    return model


def load_model_from_file(model_name, epochs):
    return load_model(MODEL_PATH_PREFIX + model_name + "_" + str(epochs))


def train_model(model, batch_size, epochs, model_name, X_train, Y_train):
    X_train, X_val, Y_train, Y_val = train_test_split(X_train, Y_train, train_size=5 / 6)
    network_history = model.fit(X_train, Y_train, batch_size=batch_size, epochs=epochs, verbose=1,
                                validation_data=(X_val, Y_val))

    model.save(MODEL_PATH_PREFIX + model_name + "_" + str(epochs))
    save_network_history_to_file(network_history, model_name, epochs)


def save_network_history_to_file(network_history, model_name, epochs):
    hist_df = pd.DataFrame(network_history.history)

    hist_json_file = MODEL_PATH_PREFIX + model_name + "_" + str(epochs) + "_history.json"
    with open(hist_json_file, mode='w') as file:
        hist_df.to_json(file)


def load_network_history_from_file(model_name, epochs):
    return pd.read_json(MODEL_PATH_PREFIX + model_name + "_" + str(epochs) + "_history.json")


def predict_classes(model, X):
    return model.predict_classes(X)
