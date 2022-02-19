from typing import AnyStr
from ..Utils.exceptions import UsersError

class User(object):
    def __init__(self, row=None, **kwargs) -> None:
        if row:
            self.id = None
            self.username = None
            self.name = None
            self.email = None
        
        elif kwargs.get('username', None):
            try:
                self.username = kwargs.pop('username')
                self.password = kwargs.pop('password')
                self.name = kwargs.pop('name', None)
                self.email = kwargs.pop('email', None)
            except KeyError as err:
                raise UsersError("Could not extract username or password values to register!") from err

        else:
            self.id = row[0]
            self.username = row[1]
            self.name = row[2]
            self.email = row[3]

    def __str__(self):
        return "{}({})".format(self.username, self.name)

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
                sql = sql.replace('[vals]', ", '{}', '{}'".format(self.name, self.email))
            else:
                sql = sql.replace('[cols]', '')
                sql = sql.replace('[vals]', '')
        else:
            raise UsersError("Could not properly set attributes into SQL query!")

        return sql

