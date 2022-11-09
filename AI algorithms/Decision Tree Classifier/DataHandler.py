#-*- conding: utf-8 -*-
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
        self.dataset = pd.read_csv(os.path.join(__location__, fileName))
        self.target = self.dataset.columns[-1]

    def encodeData(self, ordinalFeaturesMapperDict):
        ordinalEncoder = self.createOrdinalEncoder(ordinalFeaturesMapperDict)
        oneHotEncoder = self.createOneHotEncoder()
        columnTransformer = self.createColumnTransformer(ordinalFeaturesMapperDict, ordinalEncoder, oneHotEncoder)

        return columnTransformer.fit_transform(self.dataset)

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

    def createOrdinalEncoder(self, mapperDict):
        categories = []

        for features, mapper in mapperDict.items():
            for _ in range(len(features)):
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
