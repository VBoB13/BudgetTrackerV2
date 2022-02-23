from typing import Tuple
from ..Utils.exceptions import StoresError


class Store(object):
    def __init__(self, row: Tuple = None):
        self.id = None
        self.name = None
        if row is not None:
            self.id = row[0]
            self.name = row[1]

    def __str__(self):
        if self.id:
            return "{} (#{})".format(self.name, self.id)
        return "No real store.(No id detected.)"

    def __iter__(self):
        if self.id:
            yield "id", self.id
            yield "name", self.name
        else:
            raise StoresError(
                "Not iterable: no 'id'! id:{} & name:{}".format(self.id, self.name))

    @staticmethod
    def get_all_stores():
        return """
            SELECT * FROM "STORES";
        """

    @staticmethod
    def add_store(name: str):
        return """
            INSERT INTO "STORES" (name) VALUES ('{}')
        """.format(name)

    @staticmethod
    def get_store(name: str):
        return """
            SELECT * FROM "STORES" WHERE name='{}';
        """.format(name)
