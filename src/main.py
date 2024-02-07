import argparse
import time
from typing import Dict, Union

from database.Config import Config
from ingest.FileHandler import FileHandler
from repository.StockRepository import StockRepository
from store.SqlStore import SqlStore


def clean_db() -> None:
    print('>> Clean `stock` table.')
    config = Config()
    dbConnection = config.get_arrow_connection()

    store_service = SqlStore(connection=dbConnection)
    
    stockRepository = StockRepository(
        store_service=store_service,
    )
    stockRepository.clear()

    config.close_connection()


def insert_rows(file: str, chunks: int) -> None:
    print('>> Insert rows.')

    config = Config()
    dbConnection = config.get_arrow_connection()

    store_service = SqlStore(connection=dbConnection)

    stockRepository = StockRepository(store_service=store_service)

    fileHandler = FileHandler()
    iteration = 0

    while True:
        # Manipulate data by chunks.
        data = fileHandler.read_by_chunks(
            fileLocation=file,
            chunkSize=chunks,
            skipRows=chunks * iteration
        )

        if len(data) == 0:
            # No more data to used, the `while` loop to read must be finish.
            break
        
        beforeSave = time.time()

        stockRepository.save_many_rows(data)

        afterSave = time.time()

        print(f'\t>> Iteration {iteration} ends in {afterSave - beforeSave:.4f} seconds.')
        
        iteration += 1

    print(f'>> The insertion has been done using {iteration} iterations.')

    config.close_connection()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Command line service to read data and transport it into a repository.'
    )

    parser.add_argument('--chunks', dest='chunks', 
                            type=int,
                            default=250000,
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
    args: Dict[str, Union[str, bool]] = parser.parse_args().__dict__

    if args['clean']:
        clean_db()

    if args['insert']:
        insert_rows(
            file=args['csv_file'],
            chunks=args['chunks']
        )

    print('>> Data transportation where completed.\n')
