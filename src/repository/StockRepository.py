import uuid
import traceback
from typing import List

from store.SqlStore import SqlStore


class StockRepository:
    """
    Class that will interact with the data storage service.
    """
    def __init__(self, store_service: SqlStore, chunks: int = 100):
        self.__chunks = 100 if chunks < 100 else chunks
        self.__store_service = store_service

    def setChunks(self, chunks: int):
        self.__chunks = chunks

    def saveManyRows(self, data: List) -> None:
        try:
            print(f'>> Attempt to save {len(data)} rows with a chunk size of {self.__chunks}.')
            
            values: List[str] = []

            stockInsertStatement: str = "INSERT INTO stock (id, point_of_sale, product, date, stock) VALUES {values}"

            for row in range(0, len(data)):
                rowToInsert = data[row]
                values.append(
                    "(\'{}\', \'{}\', \'{}\', \'{}\', {})".format(
                        uuid.uuid4(),
                        rowToInsert['PointOfSale'],
                        rowToInsert['Product'],
                        rowToInsert['Date'],
                        rowToInsert['Stock']
                    )
                )
                
                if row > 0 and row % self.__chunks == 0:
                    valuesSeparatedByComma: str = ', '.join(values)
                    self.__store_service.execute(
                        sql=stockInsertStatement.format(values=valuesSeparatedByComma)
                    )

                    values = []

            if len(values) > 0:
                print(f'>> A final chunk of {len(values)} rows will be stored.')
                valuesSeparatedByComma: str = ', '.join(values)
                self.__store_service.execute(
                    sql=stockInsertStatement.format(values=valuesSeparatedByComma)
                )

        except Exception as err:
            traceback.print_exception(err)


    def clear(self) -> None:
        try:
            print('>> Attempt to drop the `stock` table.')

            stockDropStatement: str = 'DELETE FROM stock WHERE TRUE;'
            self.__store_service.execute(
                sql=stockDropStatement
            )
        except Exception as err:
            traceback.print_exception(err)
