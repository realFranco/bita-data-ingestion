# i call this directory "ingest" because we can retrieve data from different data sources

# file handler
import csv
from typing import Dict, List

class FileHandler:

    def __init__(self):
        self.__fileLocation: str = ''
        pass

    # def setFileLocation(self, fileLocation) -> None:
    #     self.__fileLocation = fileLocation
            

    def read(self, fileLocation: str) -> List[Dict]:
        """
        Read the files and return a list of dictionaries.
        """
        with open(fileLocation, 'r', encoding="utf-8-sig") as f:
            reader = csv.reader(f, delimiter=';')

            out: List[Dict] = []

            isTitle = True
            titles: List[str] = []

            for row in reader:
                if isTitle:
                    # Collect the titles from the `.csv` file.
                    titles = row
                    isTitle = False
                    continue
            
                out.append(dict(zip(titles, row)))

            f.close()

        return out

    def write(self, fileLocation):
        # No implemented.
        pass

    # def describeHeaders():

