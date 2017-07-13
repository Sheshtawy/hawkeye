from abstract_driver import AbstractDriver
import psycopg2

class PostgresDriver(AbstractDriver):
    """Postgresql DB Driver."""
    def __init__(self, credentials, db_name):
        super().__init__(credentials)
        self.db_name = db_name

    def _connect(self, db_name):
        pass

    def create(self, data):
        pass
