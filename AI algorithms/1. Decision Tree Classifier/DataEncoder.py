from copy import deepcopy
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.compose import make_column_transformer

class DataEncoder:

    def __init__(self, rawData, ordinalFeaturesDict):
        self.rawData = rawData
        self.ordinalFeaturesDict = ordinalFeaturesDict

        self.attrsUsed = None
        self.dataToEncode = None

    def encodeData(self, featuresToAbandon=None):
        self.setAttrUsed(list(self.rawData.columns), featuresToAbandon)
        self.dataToEncode = self.rawData[self.attrsUsed]

        ordinalEncoder = self.createOrdinalEncoder()
        oneHotEncoder = self.createOneHotEncoder()
        columnTransformer = self.createColumnTransformer(ordinalEncoder, oneHotEncoder)

        return columnTransformer.fit_transform(self.dataToEncode)

    def setAttrUsed(self, attrs, featuresToAbandon):
        if type(featuresToAbandon) == str:
            attrs.remove(featuresToAbandon)
        elif type(featuresToAbandon) == list:
            [attrs.remove(feature) for feature in featuresToAbandon]
        self.attrsUsed = attrs

    def createOrdinalEncoder(self):
        allCategories = []

        for features, categories in self.ordinalFeaturesDict.items():
            repeats = 0
            for feature in features:
                if feature in self.attrsUsed[:-1]:
                    repeats += 1
            for _ in range(repeats):
                allCategories.append(categories)

        return OrdinalEncoder(categories=allCategories)

    def createOneHotEncoder(self):
        return OneHotEncoder()

    def createColumnTransformer(self, ordinalEncoder, oneHotEncoder):
        ordinalFeatures = self.getOrdinalFeatures()
        nominalFeatures = self.getNominalFeatures(ordinalFeatures)    
        columnTransformer = make_column_transformer(
            (ordinalEncoder, ordinalFeatures),
            (oneHotEncoder, nominalFeatures),
            remainder='passthrough'
        )

        return columnTransformer

    def getOrdinalFeatures(self):
        ordinalFeatures = []

        for features in self.ordinalFeaturesDict.keys():
            for feature in features:
                if feature in self.attrsUsed[:-1]:
                    ordinalFeatures.append(feature)

        return ordinalFeatures

    def getNominalFeatures(self, ordinalFeatures):
        categoricalFeatures = self.getCategoricalFeatures()

        nominalFeatures = [feature for feature in categoricalFeatures if feature not in ordinalFeatures]

        return nominalFeatures

    def getCategoricalFeatures(self):
        featureColumns = self.dataToEncode.drop(self.rawData.columns[-1], axis=1)
        categoricalFeatures = featureColumns.select_dtypes(include=['object', 'bool']).columns

        return categoricalFeatures

    def getFeatures(self):
        return list(self.rawData.columns[:-1])

    # def splitIntoFeaturesAndTarget(self, dataSet):
    #     self.featureColumns = dataSet[:, range(dataSet.shape[1]-1)]
    #     self.targetColumn = dataSet[:, dataSet.shape[1]-1]