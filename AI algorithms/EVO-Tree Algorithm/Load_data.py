#-*- conding: utf-8 -*-
import csv
from msilib.schema import Feature
import random
import math

import os
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.model_selection import KFold
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.compose import make_column_transformer, make_column_selector
from sklearn import metrics

from six import StringIO  
from IPython.display import Image  
import pydotplus
import matplotlib.pyplot as plt

class DataHandler:

    def loadDataFrom(self, fileName):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.dataset = pd.read_csv(os.path.join(__location__, fileName))
        self.target = self.dataset.columns[-1]

    def getEncodedData(self, ordinalFeaturesMapperDict):
        oe = self.getOrdinalEncoder(ordinalFeaturesMapperDict)
        ohe = self.getOneHotEncoder()
        ct = self.getColumnTransformer(ordinalFeaturesMapperDict, oe, ohe)
        return ct.fit_transform(self.dataset)

    def getCategoricalFeatures(self):
        featureColumns = self.dataset.drop(self.target, axis=1)
        categoricalFeatures = featureColumns.select_dtypes(include=['object', 'bool']).columns
        return categoricalFeatures

    def getOrdinalFeatures(self, ordinalMappersDict):
        ordinalFeatures = []
        for features in ordinalMappersDict.keys():
            ordinalFeatures.extend(features)
        return ordinalFeatures

    def getNominalFeatures(self, ordinalFeatures):
        categoricalFeatures = self.getCategoricalFeatures()
        nominalFeatures = [feature for feature in categoricalFeatures if feature not in ordinalFeatures]
        return nominalFeatures

    def getOrdinalEncoder(self, mapperDict):
        categories = []
        for features, mapper in mapperDict.items():
            for _ in range(len(features)):
                categories.append(mapper)
        return OrdinalEncoder(categories=categories)

    def getOneHotEncoder(self):
        return OneHotEncoder()

    def getColumnTransformer(self, ordinalMapperDict, ordinalEncoder, oneHotEncoder):
        ordinalFeatures = self.getOrdinalFeatures(ordinalMapperDict)
        nominalFeatures = self.getNominalFeatures(ordinalFeatures)    
        columnTransformer = make_column_transformer(
            (ordinalEncoder, ordinalFeatures),
            (oneHotEncoder, nominalFeatures),
            remainder='passthrough'
        )
        return columnTransformer


datasetFileName = 'ObesityData.csv'
ordinalFeaturesMappers = {
    ("CAEC", "CALC"): ["no", "Sometimes", "Frequently", "Always"]
}

dataHandler = DataHandler()
dataHandler.loadDataFrom(datasetFileName)
readyData = dataHandler.getEncodedData(ordinalFeaturesMappers)
print(readyData)

# dataHandler.dataset.hist(bins=25,figsize=(10,10))
# plt.show()

# print(dataHandler.dataset.isnull().values.any())

# dataHandler.dataset



# kfold = KFold(5, shuffle=True)
# accs = []

# for i in range(5):
#     for train, test in kfold.split(readyData):
#         train_x = readyData.loc[train][features]
#         train_y = readyData.loc[train][classes]
#         test_x = readyData.loc[test][features]
#         test_y = readyData.loc[test][classes]
        
#         clf = DecisionTreeClassifier()
#         clf = clf.fit(train_x, train_y)
#         pred_y = clf.predict(test_x)
#         accs.append(metrics.accuracy_score(test_y, pred_y))

# print("mean accuracy", np.mean(accs))
# print("standard deviation", np.std(accs))

# dot_data = StringIO()
# export_graphviz(clf, out_file=dot_data,  
#                 filled=True, rounded=True,
#                 special_characters=True,feature_names = features,class_names=classes)
# graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
# graph.write_png('tree.png')
# Image(graph.create_png())