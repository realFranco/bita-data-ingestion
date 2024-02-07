import csv
import traceback
from typing import Dict, List

import pandas


class FileHandler:

    def __init__(self):
        pass

    def read(self, fileLocation: str) -> List[Dict]:
        print('>> Reading the input file.')
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
    
    def read_by_chunks(self, fileLocation: str, chunkSize: int, skipRows: int) -> List[Dict]:
        try:
            with pandas.read_csv(
                filepath_or_buffer=fileLocation,
                delimiter=';',
                chunksize=chunkSize,
                encoding='utf-8-sig',
                low_memory=False,
                skiprows=skipRows
            ) as reader:
                df = reader.get_chunk()
                data = [series[1].to_dict() for series in df.iterrows()]

                return data

        except pandas.errors.EmptyDataError as err:
            print('>> No more data will be collected.')
            
            return []

        except Exception as err:
            traceback.print_exception(value=None, tb=err, etype=BaseException)

            return []
