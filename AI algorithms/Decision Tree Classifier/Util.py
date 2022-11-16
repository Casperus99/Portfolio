import os
import pandas as pd

class Util:

    @staticmethod
    def loadDatasetFrom(fileName):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        dataset = pd.read_csv(os.path.join(__location__, fileName))

        return dataset