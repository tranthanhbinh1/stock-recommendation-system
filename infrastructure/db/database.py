from abc import ABC, abstractmethod


class Database(ABC):  # TODO: implement a Singleton pattern
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def query(self, query: str):
        pass

    @abstractmethod
    def insert(self, df, table_name, schema, exist_strat):
        pass

    @abstractmethod
    def close(self):
        pass
