import os

import adbc_driver_postgresql.dbapi


class Config:

    def __init__(self) -> None:
        self.__connection = None

    def get_arrow_connection(self) -> None:
        uri: str = f"postgresql://{os.environ.get('POSTGRES_HOST')}:5432/{os.environ.get('POSTGRES_DB')}?user={os.environ.get('POSTGRES_USER')}&password={os.environ.get('POSTGRES_PASSWORD')}"
        self.__connection = adbc_driver_postgresql.dbapi.connect(uri)

        return self.__connection

    def close_connection(self) -> None:
        self.__connection.close()
