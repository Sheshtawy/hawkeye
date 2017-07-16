import abc
import json
import jsonschema


class AbstractDriver(metaclass=abc.ABCMeta):
    """Generic interface for DB Drivers."""
    def __init__(self, **credentials):
        super().__init__()
        try:
            from source.utils.schemas.db_credentials_schema import DB_CREDENTIALS_SCHEMA
            jsonschema.validate(credentials, DB_CREDENTIALS_SCHEMA)
        except jsonschema.ValidationError as error:
            print(error)
        self.host = credentials['host']
        self.port = credentials['port']
        self.username = credentials['username']
        self.password = credentials['password']

    @abc.abstractmethod
    def create(self, data):
        """Insert a new instance."""

    @abc.abstractmethod
    def retrieve(self, instance_id):
        """Retrieve instance by id."""

    @abc.abstractmethod
    def update(self, instance_id, data):
        """Update instance."""

    @abc.abstractmethod
    def delete(self, instance_id):
        """Delete instance."""
