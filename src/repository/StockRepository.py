import traceback
from typing import Dict, List

from store.SqlStore import SqlStore


class StockRepository:
    """
    Class that will interact with the data storage service.
    """
    def __init__(self, store_service: SqlStore):
        self.__store_service = store_service

    def save_many_rows(self, data: List[Dict]) -> None:
        try:
            print(f'>> Attempt to save {len(data)} rows.')
            
            values: str = ''

            for row in range(0, len(data)):
                rowValues = list(data[row].values())
                values += "(\'{}\', \'{}\', \'{}\', {}), ".format(
                        rowValues[0],
                        rowValues[1],
                        rowValues[2],
                        rowValues[3]
                    )
                
            values = values[:-2]  # Ignore the last comma character `, `.

            self.__store_service.execute(
                sql='INSERT INTO stock (point_of_sale, product, date, stock) VALUES ' + values
            )

        except Exception as err:
            traceback.print_exception(value=None, tb=err, etype=BaseException)


    def clear(self) -> None:
        try:
            print('>> Attempt to clean the `stock` table.')

            stockDropStatement: str = 'DELETE FROM stock WHERE TRUE;'
            self.__store_service.execute(
                sql=stockDropStatement
            )

        except Exception as err:
            traceback.print_exception(value=None, tb=err, etype=BaseException)
