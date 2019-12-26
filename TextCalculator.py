import numpy as np
from numpy import linalg as la
import configparser
from collections import Counter



class TextCalculator:

    def __init__(self, sent_counter):
        # this needs to be sent in future by the caller of the constructor
        self.values_sent = sent_counter
        # read the configuration file for the calculations.
        self.config = configparser.ConfigParser()
        self.config.read("textcalculator.cfg")
        self.all_param = (self.config["CALC_PARAMETERS"]["CONSIDERED"]).split(",")  # List of the parameters
        self.diff_str, self.tot_str = (self.config["DEFAULT"]["diff_tot_string"]).split(",")
        # initialize math objects
        self.dim = len(self.all_param)
        self.matrix = np.ndarray(shape=(self.dim, self.dim))
        self.vector = np.ndarray(shape=(self.dim, 1))
        # initialize the matrix with the coefficents from the configuration
        # load the matrix with the weighting factors for the corresponding params
        self.init_matrix()

    # needed for normalisation and distributing the different parameters
    def gaussian(self, x, mu, sig):
        return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

    def init_matrix(self):
        i = 0
        j = 0
        for i in range(0, self.dim):
            for j in range(i + 1, self.dim + 1):
                try:
                    first_param = self.all_param[i]
                    sec_param = self.all_param[j]
                except IndexError:
                    first_param = self.all_param[i]
                    sec_param = "end_matrix_element"

                if (sec_param != "end_matrix_element"):
                    self.matrix[i][i] = self.config["CALC_MATRIX_COEFF"][first_param]
                    self.matrix[i][j] = self.config["CALC_MATRIX_COEFF"][first_param + "_" + sec_param]
                else:
                    self.matrix[i][i] = self.config["CALC_MATRIX_COEFF"][first_param]

        self.matrix = self.matrix / la.norm(self.matrix)

    #get and set methods
    def get_dimension(self):
        return self.dim

    def get_matrix(self):
        return self.matrix

    def get_vector(self):
        return self.vector

    def set_matrix(self, new_matrix):
        self.matrix = new_matrix

    def set_vector(self, new_vector):
        self.vector = new_vector

    def get_parameters(self):
        return self.all_param

    def get_values(self):
        return self.values_sent

    def set_values(self, new_values):
        self.values_sent = new_values

    #norms the values sent over a standard distribution. Coefficents are in the config-file
    def norm_vector(self):
        i = 0
        for param in self.all_param:
            mu, sigma = (self.config["DISTR_COEFF"][param]).split(",")
            mu = float(mu)
            sigma = float(sigma)
            if (param[-1:] == "/"):
                # ratio of the same word type
                value = self.values_sent[param[:-1] + self.diff_str] / self.values_sent[param[:-1] + self.tot_str]
                print("In Ratio:" + str(value))
            elif (param.find("/") != -1):
                # ratio of different word types
                print("Is here the problem?")
                a, b = param.split("/")
                a = a + self.tot_str
                b = b + self.tot_str
                value = self.values_sent[a] / self.values_sent[b]
            else:
                # not a ratio
                value = self.values_sent[param]

            self.vector[i][0] = self.gaussian(value, mu, sigma)
            i = i + 1
            print(self.vector)

    #returns the weighted quality percentage
    def get_percentage(self):
        self.my_result = np.dot(self.matrix, self.vector)
        return la.norm(self.my_result)
