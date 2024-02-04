import os
import psycopg2


class Config:

    def __init__(self) -> None:
        self.__connection = None

    def getConnection(self) -> None:
        self.__connection = psycopg2.connect(
            host=os.environ.get('POSTGRES_HOST'),
            database=os.environ.get('POSTGRES_DB'),
            user=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD'),
        )
        self.__connection.set_session(autocommit=True)

        return self.__connection

    def closeConnection(self) -> None:
        self.__connection.close()
