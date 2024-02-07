import csv
import traceback
from typing import Dict, List

import pandas


class FileHandler:

    def __init__(self):
        pass

    def read(self, file_location: str) -> List[Dict]:
        print('>> Reading the input file.')
        with open(file_location, 'r', encoding="utf-8-sig") as f:
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
    
    def read_by_chunks(self, file_location: str, chunk_size: int, skip_rows: int) -> List[Dict]:
        try:
            with pandas.read_csv(
                filepath_or_buffer=file_location,
                delimiter=';',
                chunksize=chunk_size,
                encoding='utf-8-sig',
                low_memory=False,
                skiprows=skip_rows
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
