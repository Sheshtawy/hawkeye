from .abstract_driver import AbstractDriver
import psycopg2
import sys
import traceback

class PostgresDriver(AbstractDriver):
    """Postgresql DB Driver."""
    def __init__(self, **credentials):
        super().__init__(**credentials)

    def _connect(self, db_name):
        conn_string = 'host={0} port={1} dbname={2} user={3} password={4}'.format(
            self.host,
            self.port,
            db_name,
            self.username,
            self.password
        )

        conn = psycopg2.connect(conn_string)
        return conn

    def create(self, db_name, table, data):
        """
        Create an instance.

        :param table: table name
        :param data: dictionary with values to be inserted
        data format has to match table's schema.
        Example:
        data = {
            "col1": "value1",
            "col2": "value2
        }
        """
        try:
            conn = self._connect(db_name)
            conn.set_session(autocommit=True)
            cursor = conn.cursor()
            col_names = data.keys()
            cols = '(' + ', '.join(list(col_names)) + ')'
            values = []
            for i in range(len(data.values())):
                values.append('%s')
            values = '(' + ', '.join(values) + ')'
            SQL = "INSERT INTO {0} ".format(table) + cols + " VALUES " + values + ';'
            cursor.execute(SQL, tuple(data.values()))
            cursor.close()
            conn.close()
        except Exception as e:
            print('Unexpected Error:', e)
            traceback.print_exc()
    
    def update(self, id):
        return

    def retrieve(self, db_name, table, field, value):
        try:
            conn = self._connect(db_name)
            conn.set_session(autocommit=True)
            cursor = conn.cursor()
            SQL = 'SELECT * FROM {0} WHERE {1}'.format(table, field) + '=%s;'
            cursor.execute(SQL, [value])
            return cursor.fetchone()
        except Exception as e:
            raise e

    def delete(self, id):
        return
