"""
File mostly necessary to store connection data to databases.
"""
import os

budtra_conn = {
    "dbname": "BT",
    "user": "postgres",
    "password": os.environ["BUDTRA_DB_PASSW"],
    "host": "localhost",
    "port": "5433"
}

if __name__ == '__main__':
    print(os.environ["BUDTRA_DB_PASSW"])