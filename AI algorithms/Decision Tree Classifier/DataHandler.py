#-*- conding: utf-8 -*-
import copy
import os
import pandas as pd
import pydotplus
import matplotlib.pyplot as plt

from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.compose import make_column_transformer
from six import StringIO  
from IPython.display import Image  


class DataHandler:

    def loadDataFrom(self, fileName):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.rawDataset = pd.read_csv(os.path.join(__location__, fileName))
        self.target = self.rawDataset.columns[-1]
        self.features = list(self.rawDataset.columns[:-1])

    def encodeData(self, ordinalFeaturesMapperDict, featureToAbandon=None):
        self.featureToAbandon = featureToAbandon
        if featureToAbandon:
            reducedFeatures = self.getReducedFeatures(featureToAbandon)
            self.dataToEncode = copy.deepcopy(self.rawDataset)[reducedFeatures]
        else:
            self.dataToEncode = copy.deepcopy(self.rawDataset)

        ordinalEncoder = self.createOrdinalEncoder(ordinalFeaturesMapperDict)
        oneHotEncoder = self.createOneHotEncoder()
        columnTransformer = self.createColumnTransformer(ordinalFeaturesMapperDict, ordinalEncoder, oneHotEncoder)

        return columnTransformer.fit_transform(self.dataToEncode)

    def getCategoricalFeatures(self):
        featureColumns = copy.deepcopy(self.dataToEncode).drop(self.target, axis=1)
        categoricalFeatures = featureColumns.select_dtypes(include=['object', 'bool']).columns

        return categoricalFeatures

    def getOrdinalFeatures(self, ordinalMappersDict):
        ordinalFeatures = []

        for features in ordinalMappersDict.keys():
            for feature in features:
                if feature != self.featureToAbandon:
                    ordinalFeatures.append(feature)

        return ordinalFeatures

    def getNominalFeatures(self, ordinalFeatures):
        categoricalFeatures = self.getCategoricalFeatures()

        nominalFeatures = [feature for feature in categoricalFeatures if feature not in ordinalFeatures]

        return nominalFeatures

    def createOrdinalEncoder(self, ordinalmapperDict):
        categories = []

        for features, mapper in ordinalmapperDict.items():
            repeats = 0
            for feature in features:
                if feature != self.featureToAbandon:
                    repeats += 1
            for _ in range(repeats):
                categories.append(mapper)

        return OrdinalEncoder(categories=categories)

    def createOneHotEncoder(self):
        return OneHotEncoder()

    def createColumnTransformer(self, ordinalMapperDict, ordinalEncoder, oneHotEncoder):
        ordinalFeatures = self.getOrdinalFeatures(ordinalMapperDict)
        nominalFeatures = self.getNominalFeatures(ordinalFeatures)    
        columnTransformer = make_column_transformer(
            (ordinalEncoder, ordinalFeatures),
            (oneHotEncoder, nominalFeatures),
            remainder='passthrough'
        )

        return columnTransformer

    def getReducedFeatures(self, featureToAbandon):
        ReducedFeatures = list(self.rawDataset.columns)
        ReducedFeatures.remove(featureToAbandon)

        return ReducedFeatures
