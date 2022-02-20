from typing import AnyStr, List, Dict

from ..Utils.exceptions import CategoriesError


class Category(object):
    def __init__(self, row=None, **kwargs):
        self.id = None
        self.name = None
        self.color = None

        if row:
            self.name = row[0]
            self.color = row[1]
            self.id = int(row[2])

        if kwargs.pop("id", None):
            try:
                self.id = kwargs.pop("id")
                self.name = kwargs.pop("name")
                self.color = kwargs.pop("color")
            except KeyError as err:
                raise CategoriesError(
                    "Could not load category attributes despite finding an 'id' in **kwargs!") from err

    def __str__(self):
        return "{} - {}".format(self.name, self.color)

    def __iter__(self):
        yield "id", self.id
        yield "name", self.name
        yield "color", self.color

    @staticmethod
    def get_all() -> AnyStr:
        """
        Returns a SQL that gets all categories from the DB.
        """
        return 'SELECT * FROM "CATEGORIES"'
