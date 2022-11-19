from typing import List, Iterator

from ..Utils.exceptions import CategoriesError
from ..db.controller import query_db


class Category(object):
    def __init__(self, row=None, **kwargs):
        self.id = None
        self.name = None
        self.color = None
        self.sum = None

        if row:
            if isinstance(row[0], tuple):
                self.id = int(row[0][0])
                self.name = row[0][1]
                self.color = row[0][2]
            else:
                self.id = int(row[0])
                self.name = row[1]
                self.color = row[2]

        if kwargs.pop("color", None):
            try:
                self.id = kwargs.pop("id")
                self.name = kwargs.pop("name")
                self.color = kwargs.pop("color")
            except KeyError as err:
                raise CategoriesError(
                    "Could not load category attributes despite finding a 'color' in **kwargs!") from err

        if kwargs.pop("sum", None):
            try:
                self.id = kwargs.pop("id")
                self.name = kwargs.pop("name")
                self.sum = kwargs.pop("sum")
            except KeyError as err:
                raise CategoriesError(
                    "Could not load category attributes despite finding a 'sum' in **kwargs!")

    def __str__(self):
        return "{}".format(self.name)

    def __iter__(self):
        yield "id", self.id
        yield "name", self.name
        if self.sum is not None:
            yield "sum", self.sum
        if self.color is not None:
            yield "color", self.color

    @staticmethod
    def get_all() -> str:
        """
        Returns a SQL that gets all categories from the DB.
        """
        return 'SELECT * FROM "CATEGORIES"'

    @staticmethod
    def add_category(name: str, color: str) -> str:
        """
        Returns a SQL query string that inserts a new category into DB.
        """
        return """
            INSERT INTO "CATEGORIES" (name, color) VALUES ('{}', '{}')
        """.format(name, color)

    @staticmethod
    def get_category_by_id(cat_id: int) -> str:
        return """
            SELECT * FROM "CATEGORIES"
            WHERE id={}
        """.format(cat_id)

    @staticmethod
    def get_category_by_name(cat_name: str) -> str:
        return """
            SELECT * FROM "CATEGORIES"
            WHERE name='{}'
        """.format(cat_name)


class CategoryList(list):
    def __init__(self, input_list: List[Category]):
        """
        Takes a list of Category data objects and creates a
        list of python Category objects.
        """
        try:
            for object in input_list:
                self.append(object)
        except CategoriesError as err:
            raise CategoriesError(
                "At least one of these aren't... right? RIGHT?!\n{}".format(
                    f"{type(object).__name__}\n" for object in input_list))

    def __iter__(self) -> Iterator[Category]:
        return super().__iter__()

    def append(self, object: Category):
        if not isinstance(object, Category):
            raise CategoriesError(
                "Try adding only Category objects to Category lists...")
        super().append(object)

    @staticmethod
    def get_all_category_colors() -> List[str]:
        obj = CategoryList([Category(object)
                           for object in query_db(Category.get_all())])
        return [obj.color for obj in obj]
