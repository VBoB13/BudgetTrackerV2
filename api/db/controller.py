import psycopg2
from psycopg2.errors import CheckViolation, ForeignKeyViolation, ConnectionFailure
from colorama import Fore, Style
from typing import List, Tuple

from ..Utils.exceptions import ControllerError
from ..db import budtra_conn

connection_str = " ".join('{}={}'.format(key, value)
                          for key, value in budtra_conn.items())


def query_db(sql: str, insert=False) -> List[Tuple] or bool:
    results = None
    conn = psycopg2.connect(connection_str)
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                if insert:
                    cur.execute("COMMIT")
                else:
                    results = cur.fetchall()
    except CheckViolation as err:
        print(Fore.RED, "\n--- ERROR ---\n")
        print(err, Style.RESET_ALL)
        raise ControllerError("Check contstraint violated!") from err

    except ForeignKeyViolation as err:
        print(Fore.RED, "\n--- ERROR ---\n")
        print(err, Style.RESET_ALL)
        raise ControllerError("Foreign key contstraint violated!") from err

    except ConnectionFailure as err:
        print(Fore.RED, "\n--- ERROR ---\n")
        print(err, Style.RESET_ALL)
        raise ControllerError("Failed to connect to database!") from err

    except Exception as err:
        print(Fore.RED, "\n--- ERROR ---\n")
        print(err, Style.RESET_ALL)
        raise ControllerError(
            "Something went wrong when trying to execute the SQL query!") from err

    finally:
        conn.close()

    if insert:
        return insert
    return results


if __name__ == '__main__':
    # To not print the password by mistake
    print(" ".join(connection_str.split(" ")[:2]))
