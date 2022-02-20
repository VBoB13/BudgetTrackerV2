from typing import AnyStr, Dict

from ..Utils.exceptions import UsersError


class User(object):
    def __init__(self, row=None, **kwargs) -> None:
        self.id = None
        self.username = None
        self.name = None
        self.email = None
        if row:
            self.id = int(row[0])
            self.username = row[1]
            self.name = row[2]
            self.email = row[3]
        elif kwargs.get('username', None):
            try:
                self.username = kwargs.pop('username')
                self.password = kwargs.pop('password')
                self.name = kwargs.pop('name', None)
                self.email = kwargs.pop('email', None)
            except KeyError as err:
                raise UsersError(
                    "Could not extract username or password values to register!") from err

    def __str__(self):
        return "{}({})".format(self.username, self.name)

    def __iter__(self) -> Dict:
        yield "id", self.id
        yield "username", self.username
        yield "name", self.name
        yield "email", self.email

    def register(self) -> AnyStr:
        sql = None
        if self.username and self.password:
            sql = """
                INSERT INTO "USERS" (username, password[cols])  VALUES ('{}', '{}'[vals])
            """.format(self.username, self.password)
            if self.name and not self.email:
                sql = sql.replace('[cols]', ', name')
                sql = sql.replace('[vals]', ", '{}'".format(self.name))
            elif self.name and self.email:
                sql = sql.replace('[cols]', ', name, email')
                sql = sql.replace(
                    '[vals]', ", '{}', '{}'".format(self.name, self.email))
            else:
                sql = sql.replace('[cols]', '')
                sql = sql.replace('[vals]', '')
            return sql
        else:
            raise UsersError(
                "Could not properly set attributes into SQL query!")

    def login(self) -> AnyStr:
        """
        Builds SQL query to get a user by the username and password provided.
        """
        sql = None
        if self.username and self.password:
            sql = """
                SELECT id, username, name, email FROM "USERS" WHERE username='{}' AND password='{}' LIMIT 1
            """.format(self.username, self.password)
        else:
            raise UsersError("Cannot login without username and/or password!")
        return sql

    @staticmethod
    def get_all_users():
        return """
            SELECT id, username, name, email FROM "USERS"
        """
