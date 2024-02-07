import traceback


class SqlStore:
    def __init__(self, connection):
        self.connection = connection

    def execute(self, sql: str) -> None:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)

                self.connection.commit()
            
            return None

        except Exception as err:
            traceback.print_exception(value=None, tb=err, etype=BaseException)
