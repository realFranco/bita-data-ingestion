import argparse
from typing import Dict, Union

from ingest.FileHandler import FileHandler
from database.Config import Config
from store.SqlStore import SqlStore
from repository.StockRepository import StockRepository


def cleanDb() -> None:
    print('>> Clean `stock` table.')
    config = Config()
    dbConnection = config.getConnection()

    store_service = SqlStore(connection=dbConnection)
    
    stockRepository = StockRepository(
        store_service=store_service,
    )
    stockRepository.clear()

    config.closeConnection()


def insertRows(file: str, chunks: int, rowLimit: int) -> None:
    print('>> Insert rows.')
    fileHandler = FileHandler()
    data = fileHandler.read(fileLocation=file)

    if rowLimit > 0:
        print(f'>> The rows to handle where limited to {rowLimit} rows.')
        data = data[:rowLimit]

    config = Config()
    dbConnection = config.getConnection()

    store_service = SqlStore(connection=dbConnection)

    stockRepository = StockRepository(
        store_service=store_service,
        chunks=chunks
    )
    stockRepository.saveManyRows(data)

    config.closeConnection()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Command line service to read data and transport it into a repository.'
    )

    
    parser.add_argument('--chunks', dest='chunks', 
                            type=int,
                            default=25000,
                            help='Chunks of data to process use during the ingestion at each step.'
                        )
    parser.add_argument('--clean', dest='clean', 
                            type=bool,
                            default=True,
                            help='Run the clean database function only.'
                        )
    parser.add_argument('--csv', dest='csv_file', 
                            default=None,
                            type=str,
                            help='File input location to read.'
                        )
    parser.add_argument('--insert', dest='insert', 
                            type=bool,
                            default=True,
                            help='Run the insert data function only.'
                        )
    parser.add_argument('--row-limit', dest='row_limit', 
                            type=int,
                            default=0,
                            help='Limit of rows to use during the transfer, `0` means no limit. ' \
                                + 'It is not recommended to use due a non-optimization step during reading.'
                        )
    args: Dict[str, Union[str, bool]] = parser.parse_args().__dict__

    if args['clean']:
        cleanDb()

    if args['insert']:
        insertRows(
            file=args['csv_file'],
            chunks=args['chunks'],
            rowLimit=args['row_limit']
        )

    print('>> Data transportation where completed.\n')
