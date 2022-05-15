from os import error
from random import choice, randint, random, uniform, randrange
import statistics as stat
import pandas as pd
import numpy as np
import time
from copy import deepcopy
from Load_data import Object, Dataset

'''
Tworzy drzewo decyzyjne
'''
class Tree:
    '''
    nodes - słownik węzłów
    max_depth - maksymalna głębokość drzewa
    splits - liczba wykonywanych podziałów podczas szukania najlepszego podziału
    '''
    def __init__(self, ft_min_max, targets, max_depth, leaf_prob = 0):
        self.nodes = {}
        self.max_depth = max_depth
        self.splits = 100
        self.leaf_prob = leaf_prob
        self.ft_min_max = ft_min_max
        self.targets = targets

    '''
    Rekurencyjna metoda budująca drzewo dla danego zbioru danych
    path - na początku trzeba wstawić pustego stringa
    features - zbiór atrybutów (jakbyśmy chcieli zrobić warunek stopu na wyczerpanie atrybutów)
    '''
    def build_tree(self, dataset, path, features):
        # Zliczenie krotności występujących objektów w danym węźle
        targets = []
        for data in dataset:
            targets.append(data.target)

        ### Warunki końcowe ###
        # Jeśli został już tylko jeden element
        if len(targets) == 1:
            self.nodes[path] = [int(targets[0])] # , len(targets), 0.0
            return 0
        # Jeśli osiągnęliśmy maksymalną głębokość
        if len(path) == self.max_depth:
            self.nodes[path] = [int(stat.mode(targets))] # , len(targets), stat.variance(targets)
            return 0
        # Jeśli zostały objekty tylko jednej klasy
        if stat.variance(targets) == 0:
            self.nodes[path] = [int(stat.mode(targets))] # , len(targets), stat.variance(targets)
            return 0

        # Poszukaj najlepszego atrybutu do podziału
        best_feature, best_threshold = self.find_feature_to_split(dataset, features)

        # Dodaj nowy węzeł
        self.nodes[path] = [best_feature, best_threshold] #, len(targets), stat.variance(targets)

        # Podziel objekty używając znalezionego podziału i stwórz poddrzewa
        left, right = self.split_records(dataset, best_feature, best_threshold)
        self.build_tree(left, path + '1', features)
        self.build_tree(right, path + '0', features)

    '''
    Przeszukuje wszystkie podane atrybutu pod kątem najlepszego podziału
    Zwraca wybrany atrybut i jego wartość progową
    '''
    def find_feature_to_split(self, records, features_available):
        # Inicjalizacja paru zmiennych
        min_var = 100
        best_threshold = 0
        best_feature = 0
        # Szukaj najlepszych podziałów dla każdego z atrybutu z osobna
        for i in range(features_available):
            mean_var, threshold = self.compute_best_feature_split(records, i)
            # Jeśli jest lepszy niż dotychczasowy najlepszy to nadpisz
            if mean_var < min_var:
                min_var = mean_var
                best_threshold = threshold
                best_feature = i
        return best_feature, best_threshold

    '''
    Przeszukuje dany atrybut szukając dla niego najlepszego podziału
    Zwraca najmniejszą wariancję i wybraną wartość progową
    '''
    def compute_best_feature_split(self, records, ft_index):
        # Znajdź zakres występujących wartości danego atrybutu
        minimum, maximum = self.find_range(records, ft_index)
        ranger = maximum - minimum
        # Inicjalizacja zmiennych
        min_mean_var = 1000
        best_threshold = 0
        # Dla liczby podziałów zależnych od parametru splits
        for i in range(1, self.splits):
            # Policz wartość progową i podziel dane względem niej
            threshold = minimum + ranger * i/self.splits
            left, right = self.split_targets(records, ft_index, threshold)
            # Jeżeli choć jeden zbiornik jest pusty to pomiń podział
            if len(left) == 0 or len(right) == 0:
                continue
            # Policz ważoną wariancję dla otrzymanych zbiorników
            mean_var = self.compute_mean_variance(left, right)
            # Jeśli jest lepsza niż dotychczasowa to nadpisz
            if mean_var < min_mean_var:
                min_mean_var = mean_var
                best_threshold = threshold
        return min_mean_var, best_threshold

    
    
    '''
    Rekurencyjnie przepuszcza wartości atrybutów jednego objektu i zwraca przewidywaną klasę
    '''
    def classify_object(self, object_features, node_path):
        # Jeśli trafimy na liść to zwróć klasę liścia
        if len(self.nodes[node_path]) == 1:
            return self.nodes[node_path][0]
        # Jeśli to węzeł to powtórz tę funkcję dla odpowiedniego dziecka węzła
        if object_features[self.nodes[node_path][0]] < self.nodes[node_path][1]:
            return self.classify_object(object_features, node_path + '1')
        else:
            return self.classify_object(object_features, node_path + '0')

    '''
    Rekurencyjnie buduje drzewo z losowymi podziałami
    '''
    def build_random_tree(self, path):

        if len(path) == self.max_depth or random() < self.leaf_prob:
            self.nodes[path] = [choice(self.targets)]
            return 0

        ft = randrange(len(self.ft_min_max))
        threshold = uniform(self.ft_min_max[ft][0], self.ft_min_max[ft][1])
        self.nodes[path] = [ft, threshold]
        self.build_random_tree(path + "1")
        self.build_random_tree(path + "0")

    '''
    Rekurencyjnie przepuszcza zestaw danych przez drzewo
    Dopisuje do każdego liścia liczbę błędnie klasyfikowanych obiektów a do węzła dodatkowo klasę większościową
    '''
    def calssify_dataset(self, dataset, node_path):
        # Jeśli to liść
        if len(self.nodes[node_path]) == 1:
            leaf_target = self.nodes[node_path][0]
            errors = 0
            # Zlicz liczbę błędnych klasyfikacji
            for data in dataset:
                if data.target != leaf_target:
                    errors += 1
            # Dopisz błędy do liścia
            self.nodes[node_path].append(errors)
        # Jeśli to zwykły węzeł
        else:
            targets = []
            errors = 0
            left = []
            right = []

            # Znajdź klasę większościową
            for data in dataset:
                targets.append(data.target)
            if len(targets) != 0:
                dominant = stat.mode(targets)
            else:
                dominant = 0
        
            for data in dataset:
                # Policz liczbę klas różniących się od klasy większościowej 
                if data.target != dominant:
                    errors += 1
                # Podziel dane na zbiorniki
                if data.features[self.nodes[node_path][0]] < self.nodes[node_path][1]:
                    right.append(data)
                else:
                    left.append(data)
            # Dopisz odpowiednie wartości do słownika węzłów
            self.nodes[node_path].extend([dominant, errors])
            # Rekurencyjne odpalenie kolejnych funkcji
            self.calssify_dataset(right, node_path + '1')
            self.calssify_dataset(left, node_path + '0')

    '''
    Przycinanie drzewa
    '''
    def pruning(self):
        # Przechowuje węzły do usunięcia
        nodes_to_prune = []
        # Sprawdź każdy węzeł pod kątem możliwości przycięcia
        for node, values in self.nodes.items():
            # Jeśli dany węzeł nie jest liściem to sprawdź czy opłaca się go zamienić na liść
            if len(values) == 4:
                errors = 0
                # Poszukaj wszystkich liści, które mają korzeń w danym węźle i dodaj ich błędy
                for node2, values2 in self.nodes.items():
                    if node2.startswith(node) and len(values2) == 2:
                        errors += values2[1]
                # Jeśli poddrzewo ma conajmniej tyle samo błędów
                if errors >= values[3]:
                    # Zamień węzeł na liść
                    self.nodes[node] = [values[2], values[3]]
                    for node3, values3 in self.nodes.items():
                        # Wpisz całe poddrzewo na listę do usunięcia
                        if node3.startswith(node) and node3 != node:
                            nodes_to_prune.append(node3)
                            self.nodes[node3] = []

            # Jeśli dany węzeł jest do usunięcia to pomiń
            if len(values) == 0:
                continue
        # Usuń węzły do usunięcia
        for node in nodes_to_prune:
            del self.nodes[node]

    def split_targets(self, records, ft_index, threshold):
        left = []
        right = []
        for record in records:
            if record.features[ft_index] < threshold:
                left.append(record.target)
            else:
                right.append(record.target)
        return left, right

    def split_records(self, records, ft_index, threshold):
        left = []
        right = []
        for record in records:
            if record.features[ft_index] < threshold:
                left.append(record)
            else:
                right.append(record)
        return left, right

    def compute_mean_variance(self, list1, list2):
        if len(list1) == 1:
            left_var = list1[0]
        else:
            left_var = stat.variance(list1)
        if len(list2) == 1:
            right_var = list2[0]
        else:
            right_var = stat.variance(list2)
        return (left_var * len(list1) + right_var * len(list2))/(len(list1) + len(list2))

    def find_range(self, records, ft_index):
        for i, record in enumerate(records):
            if i == 0:
                min = record.features[ft_index]
                max = record.features[ft_index]
            else:
                if record.features[ft_index] < min:
                    min = record.features[ft_index]
                elif record.features[ft_index] > max:
                    max = record.features[ft_index]
        return min, max      

class Evolutionary_Algorithm:

    def __init__(self, dataset):
        self.dataset = dataset
        self.dataset.split_data(0.5)
        self.trees = []
        # self.tree = Tree()

    def create_random_trees(self, qn, leaf_pb, max_depth):
        self.trees = []
        for i in range(qn):
            tree = Tree(self.dataset.find_min_max(), self.dataset.available_targets, max_depth, leaf_pb)
            tree.build_random_tree('')
            self.trees.append(tree)

    def train_tree(self, tree):
        positive = 0
        for record in self.dataset.train:
            if record.target == tree.classify_object(record.features, ''):
                positive += 1
        return positive/len(self.dataset.train)

    def measure_tree(self, tree):
        max_length = 0
        for key in tree.nodes.keys():
            if(len(key) > max_length):
                max_length = len(key)
        return max_length


    def choose_best(self, old_trees, number, fit_con):
        trees = deepcopy(old_trees)
        result = []
        selected_trees = []

        for tree in trees:
            fitness = fit_con[0] * self.train_tree(tree) - fit_con[1] * self.measure_tree(tree)
            if(len(selected_trees) < number):
                selected_trees.append([tree, fitness])
            else:
                selected_trees = sorted(selected_trees, key=lambda x: x[1])
                for index, data in enumerate(selected_trees):
                    if(fitness > data[1]):
                        selected_trees[index] = [tree, fitness]
                        break
        selected_trees = sorted(selected_trees, key=lambda x: x[1])
        #print(selected_trees[-1])
        for table in selected_trees:
            result.append(table[0])

        return result

    def mutate_tree(self, old_tree, numberOfMutations, probabilities):
        tree = deepcopy(old_tree)
        for i in range(numberOfMutations):
            node = choice(list(tree.nodes.keys()))
            if(len(tree.nodes[node]) == 1):
                if(random() < probabilities[0]):
                    tree.nodes[node] = [choice(self.dataset.available_targets)]
                else: 
                    ft = randrange(len(tree.ft_min_max))
                    threshold = uniform(tree.ft_min_max[ft][0], tree.ft_min_max[ft][1])
                    tree.nodes[node] = [ft, threshold]
                    tree.nodes[node + '0'] = [choice(tree.targets)]
                    tree.nodes[node + '1'] = [choice(tree.targets)]
            else:
                if(random() < probabilities[1]):
                    ft = randrange(len(tree.ft_min_max))
                    threshold = uniform(tree.ft_min_max[ft][0], tree.ft_min_max[ft][1])
                    tree.nodes[node] = [ft, threshold]
                else: 
                    tree.nodes[node] = [choice(tree.targets)]
                    deleting = []
                    for key in list(tree.nodes.keys()):
                        if(key.startswith(node) and key != node):
                            deleting.append(key)
                    for key in deleting:
                        del tree.nodes[key]
        return tree

    def one_generation(self, mutationParams):
        selected = self.choose_best(self.trees, 2, [50, 1])
        mutated = []
        for tree in self.trees:
            mutated.append(self.mutate_tree(tree, mutationParams[0], [mutationParams[1], mutationParams[2]]))
        selected.extend(self.choose_best(mutated, 18, [50, 1]))
        self.choose_best(selected, 1, [50, 1])
        self.trees = selected
    
    def generations(self, iterations, mutationParams):
        self.create_random_trees(20, 0.2, 7)
        bestRandom = deepcopy(self.choose_best(self.trees, 1, [50, 1])[0])
        for i in range(iterations):
            self.one_generation(mutationParams)
        ours = self.choose_best(self.trees, 1, [50, 1])[0]
        results = [self.train_tree(bestRandom), self.train_tree(ours), self.test_tree(bestRandom), self.test_tree(ours)]
        return results
        

    def test_tree(self, tree):
        positive = 0
        for record in self.dataset.test:
            if record.target == tree.classify_object(record.features, ''):
                positive += 1
        return positive/len(self.dataset.test)


                
    

if __name__ == "__main__":
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    dataset_file = 'Irysy.csv'
    dataset = Dataset(dataset_file)
    alg = Evolutionary_Algorithm(dataset)
    start = time.time()
    index = []
    # for i in range(50):
    #     index.append((i+1)*10)
    #     result = alg.generations(index[i])
    #     if(i%10 == 0): 
    #         print("still working")
    #     if(i == 0):
    #         results = [[result[0]], [result[1]], [result[2]], [result[3]]]
    #     else:
    #         for j in range(4):
    #             results[j].append(result[j])
    # df = pd.DataFrame({'Tren Random':results[0], 'Tren Alg':results[1], 'Test Random':results[2], 'Test Alg':results[3]}, index)
    #print(df)

    mutations = []
    for k in range(5):
        for i in range(5):
            for j in range(5):
                index.append(k*25 + i*5 + j)
                mutationParams = [k+1, (i+1)*0.2, (j+1)*0.2]
                result = alg.generations(100, mutationParams)

                if(j == 0): 
                    print("still working")
                if(i == 0 and j == 0 and k == 0):
                    results = [[result[0]], [result[1]], [result[2]], [result[3]]]
                else:
                    for f in range(4):
                        results[f].append(result[f])
                mutations.append(mutationParams)
                
    df = pd.DataFrame({'Mutation Params':mutations, 'Tren Random':results[0], 'Tren Alg':results[1], 'Test Random':results[2], 'Test Alg':results[3]}, index)
    print(df)
            
    end = time.time()
    #print(end - start)

