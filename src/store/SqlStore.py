from psycopg2.extensions import connection as psqlConnection
from psycopg2 import ProgrammingError


class SqlStore:
    def __init__(self, connection: psqlConnection):
        self.connection = connection

    def execute(self, sql: str) -> None:
        result = None

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchone()

            return result

        except ProgrammingError:
            # No action while the cursor do not transfer any data.
            pass
