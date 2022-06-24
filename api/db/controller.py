import psycopg2
from psycopg2.errors import CheckViolation, ForeignKeyViolation, ConnectionFailure
from colorama import Fore, Style
from typing import List, Tuple

from ..Utils.exceptions import ControllerError
from ..db import budtra_conn

connection_str = " ".join('{}={}'.format(key, value)
                          for key, value in budtra_conn.items())


def query_db(sql: str, insert=False, delete=False) -> List[Tuple] or Tuple or bool:
    results = None
    conn = None
    try:
        conn = psycopg2.connect(connection_str)
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                if not insert:
                    results = cur.fetchall()
    except CheckViolation as err:
        if conn is not None:
            cur = conn.cursor()
            with cur:
                cur.execute("ROLLBACK;")
        print(Fore.RED, "\n--- ERROR ---\n")
        print(err, Style.RESET_ALL)
        raise ControllerError("Check contstraint violated!") from err

    except ForeignKeyViolation as err:
        if conn is not None:
            cur = conn.cursor()
            with cur:
                cur.execute("ROLLBACK;")
        print(Fore.RED, "\n--- ERROR ---\n")
        print(err, Style.RESET_ALL)
        raise ControllerError("Foreign key contstraint violated!") from err

    except ConnectionFailure as err:
        if conn is not None:
            cur = conn.cursor()
            with cur:
                cur.execute("ROLLBACK;")
        print(Fore.RED, "\n--- ERROR ---\n")
        print(err, Style.RESET_ALL)
        raise ControllerError("Failed to connect to database!") from err

    except Exception as err:
        if conn is not None:
            cur = conn.cursor()
            with cur:
                cur.execute("ROLLBACK;")
        print(Fore.RED, "\n--- ERROR ---\n")
        print(err, Style.RESET_ALL)
        raise ControllerError(
            "Something went wrong when trying to execute the SQL query!") from err
    else:
        if conn is not None:
            cur = conn.cursor()
            with cur:
                cur.execute("COMMIT;")

    finally:
        if conn is not None:
            conn.close()

    if insert and delete:
        raise ControllerError(Fore.RED,
                              "Cannot delete AND insert at the same time!" + Fore.YELLOW + "\nKwargs:\n" + Style.RESET_ALL + "Insert:\t{}\nDelete:\t{}\n").format(insert, delete)
    if insert or delete:
        return
    return results


if __name__ == '__main__':
    # To not print the password by mistake
    print(" ".join(connection_str.split(" ")[:2]))
