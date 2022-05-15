from math import exp
from file_read  import WineCsvReader
import numpy as np

from random import shuffle

beta = 0.01

def activation_der(x):
    return exp(x)/((exp(x)+1)**2)

def vector_product(vect_a, vect_b):
    sum = 0
    for i, a in enumerate(vect_a):
        sum += a*vect_b[i]
    return sum 

class Neuron:
    def __init__(self, input_size):
        self.weights = []
        self.output = 0
        self.der = []
        for i in range(input_size):
            self.weights.append(0.1)

    def activation(self, input):
        z = vector_product(input, self.weights)
        self.output = exp(z)/(exp(z)+1)
        # self.output = 1/(exp(-z)+1)

        return self.output

    def end_output(self, input):
        z = vector_product(input, self.weights)
        self.output = z
        return self.output


class Layer:
    def __init__(self, size, input_size):
        self.neurons = []
        for i in range(size):
            self.neurons.append(Neuron(input_size))

    def calculate_output(self, input):
        output = []
        for neuron in self.neurons:
            output.append(neuron.activation(input))
        return output
        
    def calculate_end_output(self, input):
        output = []
        for neuron in self.neurons:
            output.append(neuron.end_output(input))
        return output


class Network:
    def __init__(self, layers_sizes, input_size):
        self.layers = []
        for i, size in enumerate(layers_sizes):
            if i == 0:
                self.layers.append(Layer(size, input_size))
            else:
                self.layers.append(Layer(size, layers_sizes[i-1]))
        
    def calculate_output(self, input):
        local_output = input
        for layer in self.layers[:-1]:
            local_output = layer.calculate_output(local_output)
        local_output = self.layers[-1].calculate_end_output(local_output)
        local_output = self.normalize(local_output)
        return local_output

    def normalize_output(self):
        layer = self.layers[-1]
        suma = 0
        for neuron in layer.neurons:
          suma += neuron.output**2

        suma = np.sqrt(suma)
        for neuron in layer.neurons:
          neuron.output = neuron.output/suma

    def normalize(self, outputs):
        suma = 0
        for output in outputs:
          suma += output**2
        suma = np.sqrt(suma)
        for output in outputs:
            output = output/suma
        return outputs

    def train(self, data, epochs):
        wine = data[0]



        for a in range(epochs):

            for wine in data:

                x=wine.create_train_data()

                y=wine.create_y_vector()
                print(y)

                print(self.calculate_output(x))
                self.normalize_output()                

                for i, layer in enumerate(reversed(self.layers)): # odwrócenie kolejności wartsw - propoagacja wsteczna
                    if i == 0:# pochodna warstwy wyjściowej
                        for  j, neuron in enumerate(layer.neurons):
                            neuron.der = []
                            for  k, back_neuron in enumerate(reversed(self.layers[i+1].neurons)):
                            # print(neuron.output)
                              neuron.der.append(2 * (-(y[j]) + neuron.output) * back_neuron.output)
                            # print(neuron.der)
                    else: # pochodne warstw ukrytych
                        if i == (len(self.layers) - 1): # ostatnia wartswa ukryta
                            dq__dy_x = []
                            for  j, neuron in enumerate(layer.neurons):
                                suma = 0 # pochodna dq__dy_xj
                                for  k, out_neuron in enumerate(reversed(self.layers[0].neurons)):
                                    suma += 2 * (-(y[k]) + out_neuron.output) * out_neuron.weights[j]
                                dq__dy_x.append(suma)

                            for  j, neuron in enumerate(layer.neurons):
                              neuron.der = []
                              for  k, input in enumerate(x):

                                neuron.der.append(dq__dy_x[j] * activation_der(neuron.output) * input)

                        else: # pozostałe warstwy ukryte
                            dq__dy_x = []
                            for  j, neuron in enumerate(layer.neurons):
                                suma = 0 # pochodna dq__dy_xj
                                for  k, out_neuron in enumerate(reversed(self.layers[0].neurons)):
                                    suma += 2 * (-(y[k]) + out_neuron.output) * out_neuron.weights[j] 
                                dq__dy_x.append(suma)

                            for  j, neuron in enumerate(layer.neurons):
                                neuron.der = []
                                for  k, back_neuron in enumerate(reversed(self.layers[i-1].neurons)):

                                    neuron.der.append(dq__dy_x[j] * activation_der(neuron.output) * back_neuron.output)
                          

                for layer in self.layers:
                  for neuron in layer.neurons:
                    
                    # print(neuron.der)
                    for i, weight in enumerate(neuron.weights):
                      neuron.weights[i] -= beta*neuron.der[i]

                    # print(neuron.weights)
            

        # print(error)

                
        return local_output




if __name__ == "__main__":
    attr = []
    path = 'winequality-red.csv'

    def two_sets(factor, data):
        """
        Devide data into two group
        """
        no = int(factor*len(data))
        train_data = data[:no]
        test_data = data[no+1:]
        return train_data, test_data

    def split_data(factor, data):
        """
        Devide data for validation
        """
        table = []
        k, m = divmod(len(data), factor)
        for i in range(factor):
            table.append(data[i*k+min(i, m):(i+1)*k+min(i+1, m)])
        return table


    def read_data(stream):

        with open(stream, newline='', encoding="utf-8") as file:
        
            raw_data = WineCsvReader(file, attr).read_file()

        return raw_data

    
    def if_ok(real_output, expected_output):
        real_max = max(range(len(real_output)), key=real_output.__getitem__)
        expected_max = max(range(len(expected_output)), key=expected_output.__getitem__)
        if real_max == expected_max:
            return True
        else:
            return False        

    factor = 0.4




    data = read_data(path)#[0:100]

    # shuffle(data)


    if factor < 1 and factor > 0:
        print("Podział na zbiór treningowy i testowy")
        train_data, test_data = two_sets(factor, data)
        n = 1
    elif factor > 1 and type(factor) == int:
        validation_data = split_data(factor, data)
        print("Walidacja danych")
        n = factor
    else:
        print("Błąd")
        # return

    E = Network([2, 5, 7], 11)
    out = E.train(data, 1)

  
    # out = E.calculate_output([1,2,3,4,5,6,7,8,9,0])



