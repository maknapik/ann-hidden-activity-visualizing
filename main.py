from network.data_loader import *
from network.network import *
from analysis.network_analysis import *
from scenarios.scenarios import *


def main():
    # X_train, Y_train, X_test, Y_test = load_data_cnn(DataType.SVHN)
    # model = create_multilayer_perceptron(DataType.MNIST)
    # train_model(model, 16, 100, "mnist_mlp", X_train, Y_train)
    # load_weights_from_file(model, "mnist_mlp", 5, 5)
    # model_cnn = create_cnn(DataType.MNIST)
    # load_weights_from_file(model_cnn, "mnist_cnn", 100, 1)
    # train_model(model_cnn, 32, 100, "mnist_cnn", X_train, Y_train)
    # model = load_model_from_file("svhn_cnn", 100)
    # network_history = load_network_history_from_file("svhn_cnn", 100)
    # plot_history(network_history)
    # l1, l2 = get_activations_cnn(model, X_test)
    # Y_predicted = predict_classes(model, X_test)
    # transformed_points, targets = show_tsne("svhn_cnn_test_l2", 100, l2[:2000], Y_test[:2000], Y_predicted[:2000])
    # print(get_knn_accuracy(transformed_points, Y_test[:2000]))
    # count_power_modulo()
    mnist_test_subset_cnn_last_hidden_layer_during_training_tsne_and_nh()


if __name__ == '__main__':
    main()
