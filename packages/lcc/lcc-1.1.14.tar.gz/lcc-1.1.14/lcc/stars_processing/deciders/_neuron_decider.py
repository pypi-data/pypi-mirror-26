import logging

import numpy as np
from pybrain import FeedForwardNetwork, LinearLayer, SigmoidLayer, FullConnection
from pybrain.datasets import ClassificationDataSet
from pybrain.structure.modules import SoftmaxLayer
from pybrain.supervised.trainers import BackpropTrainer

from lcc.entities.exceptions import QueryInputError
from lcc.stars_processing.utilities.base_decider import BaseDecider


class NeuronDecider(BaseDecider):
    """
    The class is responsible for learning to recognize certain group of objects by using NN.
    So far there just one architecture available:
        Three layered Feed Forward Network with Backpropagation Trainer:
            Input layer - LinearLayer
            Hidden layer - SigmoidLayer
            Output layer - SoftmaxLayer
        

    Attributes
    -----------
    hiden_neurons : int
        Number of hiden neurons.

    OUTPUT_NEURONS : int
        Number of output neurons.

    input_neurons : int
        Number of input neurons.

    X_train : numpy array of array of floats
        Each item of the array contains specific "coordinates" of the train
        object in array.

    X_test : numpy array of array of floats
        Each item of the array contains specific "coordinates" of the test
        object in array.

    y_train : numpy array of ints
        Each item of the array contains a number of the group which the train
        object belongs. Position in the array
        corresponds to item in X_train.

    y_test : numpy array of ints
        Each item of the array contains a number of the group which the test
        object belongs. Position in the array
        corresponds to item in X_test.

    continueEpochs : int
        Number of epochs to continue for testing after convergence

    maxEpochs : int
        Maximum number of epochs for training
    """

    OUTPUT_NEURONS = 1

    def __init__(self, threshold=0.5, hidden_neurons=2,
                 continueEpochs=50, maxEpochs=20000):
        """
        Parameters
        -----------
        hidden_neurons: int
            Number of hidden neurons

        continueEpochs : int
            Number of epochs to continue for testing after convergence

        maxEpochs : int
            Maximum number of epochs for training

        Note
        -----
        Attributes with None values will be updated by setTrainer
        and train methods
        """

        self.hiden_neurons = hidden_neurons

        self.input_neurons = None
        self.X = None
        self.y = None

        self.threshold = threshold
        self.maxEpochs = maxEpochs
        self.continueEpochs = continueEpochs

        self.net = None

    def learn(self, searched, others):
        """
        This method loads lists of specific values of searched objects and
        others. Then the sample will be  divided into train and
        test samples according to user.

        Parameters
        -----------
        searched : iterable
            List of searched objects values (their "coordinates")

        others : iterable
            List of other objects values (their "coordinates")

        Returns
        -------
        NoneType
            None
        """
        if not len(searched) or not len(others):
            raise QueryInputError("Decider can't be learned on an empty sample")

        # Resolve number of input neurons
        self.input_neurons = len(searched[0])

        # Input is accepted as a numpy array or as a list
        if type(searched) != list:
            try:
                X = searched.tolist() + others.tolist()
            except AttributeError as err:
                raise AttributeError("Wrong coordinates input: %s" % err)
        elif type(searched) == list:
            X = np.array(searched + others)

        # Note searched objects as 1 and others as 0
        self.y = np.array(
            [1 for i in range(len(searched))] + [0 for i in range(len(others))])
        self.X = X

        self.train()

    def train(self):
        """Train neuron grid by training sample"""

        self.net = FeedForwardNetwork()

        inLayer = LinearLayer(self.input_neurons)
        hiddenLayer = SigmoidLayer(self.hiden_neurons)
        outLayer = SoftmaxLayer(self.OUTPUT_NEURONS)

        self.net.addInputModule(inLayer)

        self.net.addModule(hiddenLayer)
        self.net.addOutputModule(outLayer)

        in_to_hidden = FullConnection(inLayer, hiddenLayer)
        hidden_to_out = FullConnection(hiddenLayer, outLayer)

        self.net.addConnection(in_to_hidden)
        self.net.addConnection(hidden_to_out)
        self.net.sortModules()

        ds = ClassificationDataSet(self.input_neurons, self.OUTPUT_NEURONS, nb_classes=3)
        for i, coord in enumerate(self.X):
            ds.addSample(coord, (self.y[i],))

        trainer = BackpropTrainer(self.net, dataset=ds, momentum=0.1, verbose=True, weightdecay=0.01)
        trainer.trainUntilConvergence(maxEpochs=self.maxEpochs, continueEpochs=self.continueEpochs)

        logging.info("Training of NN successfully finished")

    def evaluate(self, coords):
        """
        Find if inspected parameter-space coordinates belongs to searched
        object

        Parameter
        ---------
        coords : list of lists
            Parameter-space coordinates of inspected objects

        Returns
        ------
        numpy.array
            Probabilities of membership to searched group objects
        """
        pred = []
        for coord in coords:
            p = self.net.activate(coord)[0]
            if p < 0:
                p = 0
            elif p > 1:
                p = 1
            pred.append(p)

        return np.array(pred)
