from Load_data import Dataset, Object
from math import exp
import numpy as np
import random

# def relu(x):
#     if x > 0:
#         return x
#     else:
#         return 0

# def relu_der(x):
#     if x > 0:
#         return 1
#     else:
#         return 0

# def sigm(x):
#     return 1/(exp(-x)+1)

# def sigm_der(x):
#     return exp(x)/((exp(x)+1)**2)

def activ_fun_der(x):
    if x > 0:
        return 1
    else:
        return 0
    # return exp(x)/((exp(x)+1)**2)

def softmax(vector):
    sum = 0
    for i, scalar in enumerate(vector):
        vector[i] = exp(scalar)
        sum += vector[i]
    for i, scalar in enumerate(vector):
        vector[i] = scalar/sum

def vector_multiply_by_scalar(vector, scalar):
    new_vect = []
    for i, element in enumerate(vector):
        new_vect.append(element*scalar)
    return new_vect

def vector_multiplication(vect_a, vect_b):
    out_vect = []
    for i, element in enumerate(vect_a):
        out_vect.append(element*vect_b[i])
    return out_vect


class Neuron:

    def __init__(self, input_width, hidden=True):
        self.hidden = hidden
        self.weights = []
        self.correction = []
        self.summed_inputs = 0
        self.output = 0
        self.der = 0
        # Init zakłada, że input ma offset
        for i in range(input_width):
            self.weights.append(random.uniform(0, 0.2))

    def activation(self, input):
        '''
        Oblicza wyjście neuronu w zależności czy jest w warstwie ukrytej czy wyjściowej
        '''
        # Policz ważoną sumę
        z = self.__vector_product(input, self.weights)
        self.summed_inputs = z
        # W zależności od rodzaju wartswy oblicz wyjście
        if self.hidden:
            self.output = self.activation_function(z)
        else:
            self.output = z
        return self.output

    def __vector_product(self, vect_a, vect_b):
        '''
        Iloczyn wektorowy
        '''
        sum = 0
        for i, a in enumerate(vect_a):
            sum += a*vect_b[i]
        return sum 

    def update(self, beta):
        '''
        Uwzględnij poprawkę i wyzeruj pochodną cząstkową oraz wektor poprawek
        '''
        for i, weight in enumerate(self.weights):
            self.weights[i] -= beta*self.correction[i]
        self.correction = []
        self.der = 0

    def activation_function(self, x):
        if x > 0:
            return x
        else:
            return 0
        # return 1/(exp(-x)+1)



class Layer:

    def __init__(self, width, input_width, hidden=True):
        self.neurons = []
        self.output = []
        self.hidden = hidden
        # Init zakłada, że input ma offset
        for i in range(width):
            self.neurons.append(Neuron(input_width, hidden))
   
    def calculate_output(self, input):
        '''
        Oblicza wektor wyjściowy warstwy. Dokłada do wektora wejściowego offset na końcu
        '''
        # Dodaj offset
        input.append(1)
        # Wyzeruj dotychczasowy wektor wyjściowy
        output = []
        # Oblicz wyjścia neuronów
        for neuron in self.neurons:
            output.append(neuron.activation(input))
        # Jeśli warstwa ukryta nic nie zmieniaj
        if self.hidden:
            self.output = output
            return output
        # Jeśli warstwa wyjściowa użyj softmax i aktualizuj wyjścia neuronów
        else:
            softmax(output)
            self.output = output
            for i, neuron in enumerate(self.neurons):
                neuron.output = output[i]
            return output        


class Network:
    
    def __init__(self, layers_widths, input_size, beta):
        self.beta = beta
        self.layers = []
        # Init zakłada, że input nie ma offsetu dlatego trzeba powiększyć odpowiednie wymiary
        for i, size in enumerate(layers_widths):
            # Pierwsza warstwa ukryta
            if i == 0:
                self.layers.append(Layer(size, input_size+1))
            # Warstwa wyjściowa
            elif i == len(layers_widths)-1:
                self.layers.append(Layer(size, layers_widths[i-1]+1, False))
            # Pozostałe warstwy ukryte
            else:
                self.layers.append(Layer(size, layers_widths[i-1]+1))

    def calculate_output(self, input):
        '''
        Oblicza prawdopodobieństwa przypisania danego wektora wejściowego da każdej z możliwych klas
        '''
        local_output = input
        # Wyjście staje się wejściem
        for layer in self.layers:
            local_output = layer.calculate_output(local_output)
        # Globalne wyjście
        return local_output

    def train_once(self, input, expected_target):
        '''
        Na podstawie jednego wektoru wejściowego uczy wszystkie neurony
        '''
        # Policz wyjście globalne
        output = self.calculate_output(input)
        # Odwróć kolejność warstw
        rev_layers = self.layers[::-1]
        for i, layer in enumerate(rev_layers):
            # Dla warstwy wyjściowej
            if i == 0:
                prev_layer = rev_layers[1]
                for j, neuron in enumerate(layer.neurons):
                    # Policz pochodną cząstkową neuronu
                    neuron.der = (2*(output[j] - expected_target[j]))
                    # Policz wektor poprawek
                    neuron.correction = vector_multiply_by_scalar(prev_layer.output, neuron.der)
            # Dla warstw ukrytych
            else:
                next_layer = rev_layers[i-1]
                for j, neuron in enumerate(layer.neurons):
                    # Zsumuj iloczyny pochodnych kolejnych neuronów z odpowiednimi wagami
                    for k, next_neuron in enumerate(next_layer.neurons):
                        neuron.der += next_neuron.der*next_neuron.weights[j]
                    # Jeśli pierwsza warstwa ukryta
                    if i == (len(rev_layers) - 1):
                        neuron.correction = vector_multiply_by_scalar(input, neuron.der*activ_fun_der(neuron.summed_inputs))
                    # Pozostałe warstwy ukryte
                    else:
                        prev_layer = rev_layers[i+1]
                        neuron.correction = vector_multiply_by_scalar(prev_layer.output, neuron.der*activ_fun_der(neuron.summed_inputs))

        # Usuń dodaną jedynkę do wektora wejściowego
        del input[-1]

        self.__update_neurons()
        return output

    def __update_neurons(self):
        '''
        Zastosuj poprawki do wszystkich neuronów
        '''
        for layer in self.layers:
            for neuron in layer.neurons:
                neuron.update(self.beta)


class Experiment:

    def __init__(self, data_file, hidden_layers_widths, beta):
        self.dataset = Dataset(data_file)
        self.dataset.normalize_features()
        self.dataset.neural_network_target()
        layers_widths = hidden_layers_widths.copy()
        layers_widths.append(len(self.dataset.available_targets))
        self.classifier = Network(layers_widths, self.dataset.ft_quantity, beta)

    def train_epoch(self, data):
        '''
        Jedna epoka trenowania. Zwraca skuteczność
        '''
        correct_assumptions = 0
        for object in data:
            prediction = self.classifier.train_once(object.features, object.target)
            # Sprawdź czy spodziewana klasa pokrywa się z rzeczywistą
            if np.argmax(prediction) == np.argmax(object.target):
                correct_assumptions += 1
        #Zwróć skuteczność
        return correct_assumptions/len(data)

    def train(self, data, epochs):
        '''
        Trenuj przez podaną liczbę epok. Zwraca skuteczność
        '''
        accuracies = []
        for i in range(epochs):
            accuracies.append(self.train_epoch(data))
        return accuracies

    def test(self, data):
        '''
        Przetestuj aktualną sieć na zbiorze danych. Zwraca skuteczność
        '''
        correct_assumptions = 0
        for object in data:
            prediction = self.classifier.calculate_output(object.features)
            # Sprawdź czy spodziewana klasa pokrywa się z rzeczywistą
            if np.argmax(prediction) == np.argmax(object.target):
                correct_assumptions += 1
        return correct_assumptions/len(data)

    def train_and_test(self, epochs, ratio):
        '''
        Trenuj i przetestuj nauczoną sieć. Zwraca skuteczność ostatniej epoki i testowania
        '''
        self.dataset.split_data(ratio)
        train_accuracy = self.train(self.dataset.train, epochs)[-1]
        test_accuracy = self.test(self.dataset.test)
        return train_accuracy, test_accuracy


if __name__ == "__main__":
    #TODO
    #Standaryzacja względem wszystkich danych
    #Podział na mini-batche
    #Zapisywanie najlepszej epoki
    #Przycinanie uczenia się gdy mała zmiana błędu na testującym

    # wynik = test.calculate_output([0.1, 0.3, 0.5])
    # wynik = test.train_once([0.1, 0.3, 0.5],[0, 1, 0, 0])

    data_file = "winequality-red.csv"
    
    # hidden_layers_widths = [2]
    # for i in range(20):
    #     beta = 0.001 * (i+1)
    #     print("Beta = " + str(beta))
    #     test = Experiment(data_file, hidden_layers_widths, beta)
    #     train_accuracy, test_accuracy = test.train_and_test(100, 0.4)
    #     print(">Last train accuracy: " + str(train_accuracy))
    #     print(">Test accuracy: " + str(test_accuracy))
    #     del test
    # beta = 0.01
    # hidden_layers_widths = [1]
    # for i in range(10):
    #     hidden_layers_widths = [i+1]
    #     print("Liczba neuronów: " + str(hidden_layers_widths))
    #     test = Experiment(data_file, hidden_layers_widths, beta)
    #     train_accuracy, test_accuracy = test.train_and_test(50, 0.5)
    #     print(">Last train accuracy: " + str(train_accuracy))
    #     print(">Test accuracy: " + str(test_accuracy))
    #     del test

    beta = 0.019
    hidden_layers_widths = [8]
    print("Beta = " + str(beta))
    for i in range(5):
        test = Experiment(data_file, hidden_layers_widths, beta)
        train_accuracy, test_accuracy = test.train_and_test(300, 0.5)
        print(">Last train accuracy: " + str(train_accuracy))
        print(">Test accuracy: " + str(test_accuracy))
    
    pass
