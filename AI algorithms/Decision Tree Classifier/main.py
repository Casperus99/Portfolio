from DataHandler import DataHandler
from DecisionTreeHandler import DecisionTreeHandler
import numpy as np


if __name__ == "__main__":

    datasetFileName = 'ObesityData.csv'
    ordinalFeaturesMappers = {
        ("CAEC", "CALC"): ["no", "Sometimes", "Frequently", "Always"]
    }

    dataHandler = DataHandler()
    dataHandler.loadDataFrom(datasetFileName)
    preparedData = dataHandler.encodeData(ordinalFeaturesMappers)

    # dataHandler.dataset.hist(bins=25,figsize=(10,10))
    # plt.show()

    # print(dataHandler.dataset.isnull().values.any())

    accuracyList = DecisionTreeHandler().repeatKFoldsNTimes(preparedData, 10, 10)
    print("mean accuracy", np.mean(accuracyList))
    print("standard deviation", np.std(accuracyList))

    # dot_data = StringIO()
    # export_graphviz(clf, out_file=dot_data,  
    #                 filled=True, rounded=True,
    #                 special_characters=True)
    # graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
    # graph.write_png('tree.png')
    # Image(graph.create_png())