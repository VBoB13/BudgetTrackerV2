import psycopg2
from colorama import Fore, Style

from ..Utils.exceptions import ControllerError
from ..db import budtra_conn

connection_str = " ".join('{}={}'.format(key, value) for key, value in budtra_conn.items())
con = None

def query_db(sql: str, insert=False):
    results = None
    try:
        with psycopg2.connect(connection_str) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                if insert:
                    cur.execute("COMMIT")
                else:
                    results = cur.fetchall()
                con = conn
                
    except Exception as err:
        print(Fore.RED, "\n--- ERROR ---\n")
        print(err, Style.RESET_ALL)
        raise ControllerError from err.with_traceback(err.__traceback__)
    
    finally:
        con.close()
    
    if insert:
        return insert
    return results

if __name__ == '__main__':
    # To not print the password by mistake
    print(" ".join(connection_str.split(" ")[:2]))