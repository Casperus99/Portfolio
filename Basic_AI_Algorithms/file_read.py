#-*- coding: utf-8 -*-
import csv
from wine import Wine


class WineCsvReader:

    def __init__(self, stream, attr):
        self.reader = csv.DictReader(stream)
        self.attr = attr

    def read_file(self):
        """
        Read file
        """
        result = []

        for row in self.reader:
            result.append(self._create_wine_from(row))
        return result

    def _create_wine_from(self, row):
        """
        Create a Wine class object
        """
        return Wine(row, self.attr)

