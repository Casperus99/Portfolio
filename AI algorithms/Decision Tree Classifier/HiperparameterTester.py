import pandas as pd
from sklearn.model_selection import KFold
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
from copy import deepcopy


class HiperparameterTester:

    def __init__(self, dataset=None):
        self.kFolds = 10
        self.repeats = 10
        self.maxDepth = None

        self.featureColumns = None
        self.targetColumn = None
        if dataset is not None:
            self.splitIntoFeaturesAndTarget(dataset)

        self.accuracies = []
        self.nodeCounts = []

    def testModel(self):
        self.accuracies = []
        self.nodeCounts = []

        for _ in range(self.repeats):
            self.performKFolds()

    def performKFolds(self):
        for train, test in KFold(self.kFolds, shuffle=True).split(self.featureColumns):
            self.treeLearning(train, test)

    def treeLearning(self, train, test):
        X_train, X_test = self.featureColumns[train], self.featureColumns[test]
        y_train, y_test = self.targetColumn[train], self.targetColumn[test]

        decisionTree = DecisionTreeClassifier(max_depth=self.maxDepth)
        decisionTree.fit(X_train, y_train)

        self.accuracies.append(HiperparameterTester.testDecisionTree(decisionTree, X_test, y_test)) 
        self.nodeCounts.append(decisionTree.tree_.node_count)

    def splitIntoFeaturesAndTarget(self, dataSet):
        self.featureColumns = dataSet[:, range(dataSet.shape[1]-1)]
        self.targetColumn = dataSet[:, dataSet.shape[1]-1]

    @staticmethod
    def testDecisionTree(trainedTree, X_test, y_test):
        predictions = trainedTree.predict(X_test)
        accuracy = metrics.accuracy_score(y_test, predictions)

        return accuracy

    def setDataset(self, dataset):
        self.splitIntoFeaturesAndTarget(dataset)

    def setMaxDepth(self, maxDepth):
        self.maxDepth = maxDepth

    def setKFolds(self, kFolds):
        self.kFolds = kFolds

    def setRepeats(self, repeats):
        self.repeats = repeats

    def getAccuracies(self):
        return self.accuracies

    def getNodeCounts(self):
        return self.nodeCounts