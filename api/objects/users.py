from typing import AnyStr, Dict
from pydantic import EmailStr

from ..Utils.exceptions import UsersError


class User(object):
    def __init__(self, row=None, **kwargs) -> None:
        self.id = None
        self.username: str = None
        self.name: str = None
        self.email: EmailStr = None
        if row:
            self.id = int(row[0])
            self.username: str = row[1]
            self.name: str = row[2]
            self.email: EmailStr = row[3]
        elif kwargs.get('username', None):
            try:
                self.username: str = kwargs.pop('username')
                self.password = kwargs.pop('password')
                self.name: str = kwargs.pop('name', None)
                self.email: EmailStr = kwargs.pop('email', None)
            except KeyError as err:
                raise UsersError(
                    "Could not extract username or password values to register!") from err

    def __str__(self):
        return "{}".format(self.name)

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
    def get_user_by_id(user_id: int) -> str:
        return """
            SELECT id, username, name, email FROM "USERS" WHERE id={}
        """.format(user_id)

    def get_user_by_username(self):
        """
        Builds SQL query to get a user its the username.
        """
        sql = None
        if self.username:
            sql = """
                SELECT id, username, name, email FROM "USERS" WHERE username='{}'
            """.format(self.username)
        else:
            raise UsersError("Cannot get user by username without username!")
        return sql

    @staticmethod
    def get_all_users():
        return """
            SELECT id, username, name, email FROM "USERS"
        """
