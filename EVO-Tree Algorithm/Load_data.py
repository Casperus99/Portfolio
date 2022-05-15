#-*- conding: utf-8 -*-
import csv
import os
import random
import math

class Object:

    def __init__(self, features, target):
        self.features = features
        self.target = target


class Dataset:

    def __init__(self, file):
        self.data = []
        self.train = []
        self.test = []
        self.ft_quantity = 0
        self.available_targets = []
        self.__load_data(file)

    '''
    Wczytuje plik csv i uzupełnia zbiór danych obiektami
    '''
    def __load_data(self, file):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__, file), newline='') as f:
            reader = csv.reader(f)
            self.data = list(reader)
        # Dla każdego rekordu
        for i, record in enumerate(self.data):
            # Zamień wszystkie jego wartości na floaty
            for j, value in enumerate(record):
                self.data[i][j] = float(value)
            # Zamień go na obiekt klasy Object
            self.data[i] = Object(self.data[i][:-1], self.data[i][-1])
        # Zlicz liczbę atrybutów
        self.ft_quantity = len(self.data[0].features)
        # Znajdź wszystkie dostępne klasy
        for object in self.data:
            if object.target not in self.available_targets:
                self.available_targets.append(object.target)
        self.available_targets.sort()

    def split_data(self, ratio):
        random.shuffle(self.data)
        local_train = []
        local_test = []
        threshold = math.ceil(ratio * len(self.data))
        for i, object in enumerate(self.data):
            if i <= threshold:
                local_train.append(object)
            else:
                local_test.append(object)
        self.train = local_train
        self.test = local_test

    def find_min_max(self):
        ft_min_max = []
        for i in range(self.ft_quantity):
            ft_min_max.append([99999, -99999])

        for record in self.train:
            for index, ft in enumerate(record.features):
                if ft < ft_min_max[index][0]:
                    ft_min_max[index][0] = ft
                elif ft > ft_min_max[index][1]:
                    ft_min_max[index][1] = ft

        return ft_min_max

    '''
    Normalizuje liniowo wartości atrybutów w przedziale od 0 do 1
    '''
    # def normalize_features(self):
    #     # Do przetrzymywania wartości maksymalnych i minimalnych kolejnych atrybutów
    #     buffer = []
    #     # Wypełnij bufor, by go potem móc łatwo aktualizować
    #     for i in range(self.ft_quantity):
    #         buffer.append([0, 0])
    #     # Dla każdego objektu
    #     for i, object in enumerate(self.data):
    #         # Dla pierwszego przepisz jego wartości jako min i max jednocześnie
    #         if i == 0:
    #             for j, ft_value in enumerate(object.features):
    #                 buffer[j] = [ft_value, ft_value]
    #         # Dla kolejnych sprawdź czy któryś z jego atrybutów nie jest nowym min lub max
    #         else:
    #             for j, ft_value in enumerate(object.features):
    #                 if ft_value < buffer[j][0]:
    #                     buffer[j][0] = ft_value
    #                 elif ft_value > buffer[j][1]:
    #                     buffer[j][1] = ft_value
    #     # Zaktualizuj wszystkie wartości atrybutów we wszystkich obiektach
    #     for i, object in enumerate(self.data):
    #         for j, ft_value in enumerate(object.features):
    #             self.data[i].features[j] =  (self.data[i].features[j] - buffer[j][0]) / (buffer[j][1] - buffer[j][0])

    '''
    Zamienia klasy objektów na spodziewane wektory dla sieci neuronowej
    '''
    # def neural_network_target(self):
    #     # Stwórz domyślny spodziewany wektor o odpowiedniej długości
    #     deafult = []
    #     for i in range(len(self.available_targets)):
    #         deafult.append(0)
    #     # W zależności od klasy obiektu zastąp odpowiedni element wektora jedynką i aktualizuj obiekt
    #     for i, object in enumerate(self.data):
    #         buffer = deafult.copy()
    #         index = self.available_targets.index(object.target)
    #         buffer[index] = 1
    #         self.data[i].target = buffer
