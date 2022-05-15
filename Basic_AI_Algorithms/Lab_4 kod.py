import csv
import os
from math import pi, e
import random


class FoundClass:
    def __init__(self, quality, observation):
        self.quality = int(quality)
        self.probability = float
        self.attributes = []
        for value in observation[0:len(observation)]:
            self.attributes.append([value])
    
    def _add_observation(self, observ):
        for attr in range(len(self.attributes)):
            self.attributes[attr].append(observ[attr])

    def _find_class_probability(self, dataset_length):
        self.probability = len(self.attributes[0])/dataset_length

    def _find_normal_distribution(self):
        EX = 0
        VX = 0
        for index, attr in enumerate(self.attributes):
            EX = sum(attr)/len(attr)
            VX = self._variance(attr, EX)
            if VX == 0.0:
                VX = 10**(-99)
            self.attributes[index] = [EX, VX]

    def _variance(self, attribute_observations, EX):
        sum = 0
        for obervation in attribute_observations:
            sum += (obervation - EX)**2
        if len(attribute_observations) == 1:
            return 10**(-99)
        else:
            return sum/(len(attribute_observations)-1)


class Experiment:
    def __init__(self, data_file):
        self.data_file = data_file
        self.data = []
        self.folds = []
        self.training_dataset = []
        self.testing_dataset = []
        self.classes = []
        self._load_data()

    def evaluate_dividing(self, training_volume, repetitions):
        mean_efficiency = 0
        for repetition in range(repetitions):
            self.classes = []
            self._data_division(training_volume)
            mean_efficiency += self._find_efficiency()
        return mean_efficiency/repetitions

    def evaluate_crossing(self, n_folds, repetitions):
        mean_efficiency = 0
        for repetition in range(repetitions):
            whole_crossing_efficiency = 0
            self.classes = []
            self._data_crossing(n_folds)
            for fold_index in range(len(self.folds)):
                self._crossing_merge(fold_index)
                whole_crossing_efficiency += self._find_efficiency()
            mean_efficiency += whole_crossing_efficiency/n_folds
        return mean_efficiency/repetitions
    
    def _load_data(self):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__, self.data_file), newline='') as f:
            reader = csv.reader(f)
            self.data = list(reader)
            self.data.pop(0)
        for record in range(len(self.data)):
            self.data[record]= self.data[record][0].split(';')
            for value in range(len(self.data[record])):
                self.data[record][value] = float(self.data[record][value])

    def _find_efficiency(self):
        self._train()
        efficiency = 0
        for test in self.testing_dataset:
            prediction = self._find_class(test[0:11])
            real_class = int(test[11])
            if prediction == real_class:
                efficiency += 1
        return efficiency/len(self.testing_dataset)

    def _data_division(self, training_volume):
        mixed_data = random.sample(self.data, len(self.data))
        self.training_dataset = mixed_data[0:training_volume]
        self.testing_dataset = mixed_data[training_volume:len(self.data)]

    def _data_crossing(self, n_folds):
        self.folds = []
        for n in range(n_folds):
            self.folds.append([])
        for index, example in enumerate(random.sample(self.data, len(self.data))):
                  self.folds[index % n_folds].append(example)

    def _crossing_merge(self, test_fold_index):
        self.testing_dataset = self.folds[test_fold_index]
        self.training_dataset = []
        for index in range(len(self.folds)):
            if index != test_fold_index:
                self.training_dataset.extend(self.folds[index])

    def _train(self):
        self.classes = []
        self._fill_classes_up_with_observations()
        for found_class in self.classes:
            found_class._find_class_probability(len(self.training_dataset))
            found_class._find_normal_distribution()

    # part of the _train function
    def _fill_classes_up_with_observations(self):
        for observation in self.training_dataset:
            for found_class in self.classes:
                if int(observation[11]) == found_class.quality:
                    found_class._add_observation(observation[0:11])
                    break
            else:
                self.classes.append(FoundClass(int(observation[11]), observation[0:11]))
            
    def _find_class(self, observation):
        estimated_class = 0
        best_probability = 0
        for found_class in self.classes:
            probability = found_class.probability
            for index, attr in enumerate(found_class.attributes):
                probability *= self._normal_distribution(attr[0], attr[1], observation[index])
            if probability > best_probability:
                best_probability = probability
                estimated_class = found_class.quality
        return estimated_class

    # Used only in _find_class function
    def _normal_distribution(self, EX, VX, attr):
        exp = -((attr-EX)**2)/(2*VX)
        nominator = e**exp
        denominator = (2*pi*VX)**0.5
        return nominator/denominator


if __name__ == "__main__":
    dataset_file = 'winequality-red.csv'
    training_volume = 1000
    k = 5 
    # result1 = Experiment(dataset_file).evaluate_crossing(k, 15)
    result1 = Experiment(dataset_file).evaluate_dividing(training_volume, 20)
    print(result1)