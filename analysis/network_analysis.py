from os.path import exists

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from keras import backend as K
from sklearn.manifold import TSNE
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

from network.constants import TSNE_PATH_PREFIX


def plot_history(network_history):
    plt.figure()
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.plot(network_history['loss'])
    plt.plot(network_history['val_loss'])
    plt.legend(['Training', 'Validation'])

    plt.figure()
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.plot(network_history['accuracy'])
    plt.plot(network_history['val_accuracy'])
    plt.legend(['Training', 'Validation'], loc='lower right')
    plt.show()


def get_activations_mlp(model, data):
    layer_output = K.function([model.layers[0].input],
                              [model.layers[0].output, model.layers[2].output, model.layers[4].output,
                               model.layers[6].output])

    return layer_output([data[:2000, :]])


def get_activations_cnn(model, data, size=None):
    layer_output = K.function([model.layers[0].input], [model.layers[9].output, model.layers[10].output])
    if size:
        return layer_output([data[:size, :]])
    return layer_output([data[:2000, :]])


def show_tsne(model_name, epochs, X, Y, Y_predicted=None, init=None):
    data = StandardScaler().fit_transform(X)
    targets = np.argmax(Y, axis=1)

    file_path = TSNE_PATH_PREFIX + model_name + "_" + str(epochs) + ".npy"
    if exists(file_path):
        points_transformed = np.load(file_path)
    else:
        if init is not None:
            points_transformed = TSNE(n_components=2, perplexity=30, init=init,
                                      random_state=np.random.RandomState(0)).fit_transform(data).T
            np.save(file_path, points_transformed)
        else:
            points_transformed = TSNE(n_components=2, perplexity=30,
                                      random_state=np.random.RandomState(0)).fit_transform(data).T
            np.save(file_path, points_transformed)
    points_transformed = np.swapaxes(points_transformed, 0, 1)

    show_scatterplot(points_transformed, targets, Y_predicted)

    return points_transformed, targets


def show_scatterplot(points_transformed, targets, Y_predicted=None):
    if type(Y_predicted) == None:
        palette = sns.color_palette("bright", 10)
        plt.figure(figsize=(10, 10))
        sns.scatterplot(points_transformed[:, 0], points_transformed[:, 1], hue=targets, legend='full', palette=palette)
        plt.show()
    else:
        Y_diff = targets - Y_predicted
        styles = np.empty(shape=[0, 1], dtype=str)
        for y in Y_diff:
            if y == 0:
                styles = np.append(styles, 'Matched')
            else:
                styles = np.append(styles, 'Mismatched')

        palette = sns.color_palette("bright", 10)
        plt.figure(figsize=(10, 10))
        sns.scatterplot(points_transformed[:, 0], points_transformed[:, 1], hue=targets, style=styles,
                        legend='full', palette=palette)
        plt.show()


def get_knn_accuracy(X, Y):
    knn = NearestNeighbors(n_neighbors=7)
    knn.fit(X)

    ratio = 0
    Y = np.argmax(Y, axis=1)
    for neighbors in knn.kneighbors(X, return_distance=False):
        count = 0
        for neighbor in neighbors[1:]:
            if Y[neighbors[0]] == Y[neighbor]:
                count += 1
        ratio += count / 6

    return ratio / X.shape[0]

def plot_neuron_projection(x, Y):
    # plt.figure(figsize=(5, 5))
    # plt.scatter(x[:, 0], x[:, 1])
    # plt.show()
    # targets = np.argmax(Y, axis=1)
    plt.figure(figsize=(10, 10))
    # palette = sns.color_palette("bright", 10)
    print('plotting',x.shape)
    print(x)
    sns.scatterplot(x[:, 0], x[:, 1])
    plt.show()
