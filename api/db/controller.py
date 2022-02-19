import psycopg2
from colorama import Fore, Style

from ..Utils.exceptions import ControllerError
from ..db import budtra_conn

connection_str = " ".join('{}={}'.format(key, value) for key, value in budtra_conn.items())

def get_db(sql: str):
    results = None
    try:
        with psycopg2.connect(connection_str) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
    except Exception as err:
        print(Fore.RED, "\n--- ERROR ---\n")
        print(err, Style.RESET_ALL)
        raise ControllerError from err
    else:
                results = cur.fetchall()
    finally:
        conn.close()
    
    return results

if __name__ == '__main__':
    # To not print the password by mistake
    print(" ".join(connection_str.split(" ")[:2]))