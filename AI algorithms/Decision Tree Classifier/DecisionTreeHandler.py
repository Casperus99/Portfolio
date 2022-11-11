from sklearn.model_selection import KFold
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics

class DecisionTreeHandler:

    def __init__(self, maxDepth=None):
        self.maxDepth = maxDepth
         
        self.accs = []

    def repeatKFoldsNTimes(self, dataset, kFolds, nTimes):
        self.accs = []
        featureColumns, targetColumn = DecisionTreeHandler.featuresTargetColumnsSplit(dataset)

        for _ in range(nTimes):
            self.accs.extend(self.performKFolds(kFolds, featureColumns, targetColumn))

        return self.accs

    def performKFolds(self, k, featureColumns, targetColumn):
        accuracyList = []

        for train, test in KFold(k, shuffle=True).split(featureColumns):
            X_train, X_test = featureColumns[train], featureColumns[test]
            y_train, y_test = targetColumn[train], targetColumn[test]
            trainedTree = DecisionTreeClassifier(max_depth=self.maxDepth).fit(X_train, y_train)
            acc = DecisionTreeHandler.testDecisionTree(trainedTree, X_test, y_test)
            accuracyList.append(acc)

        return accuracyList

    def featuresTargetColumnsSplit(dataSet):
        featureColumns, targetColumn = dataSet[:, range(dataSet.shape[1]-1)], dataSet[:, dataSet.shape[1]-1]

        return featureColumns, targetColumn

    def testDecisionTree(trainedTree, X_test, y_test):
        predictions = trainedTree.predict(X_test)
        accuracy = metrics.accuracy_score(y_test, predictions)

        return accuracy
