import mnist_loader

training_data, validation_data, test_data = mnist_loader.load_data_wrapper()

import network1 as network
n_neurons = 20
net = network.Network([784 , n_neurons, 10])

n_epochs, batch_size, eta = 30, 10, 3.0
net.SGD(training_data , n_epochs, batch_size, eta, test_data = test_data)