"""
File mostly necessary to store connection data to databases.
"""
import os

budtra_conn = {
    "dbname": "budgettracker",
    "user": "postgres",
    "password": os.environ["BUDTRA_DB_PASSW"]
}

if __name__ == '__main__':
    print(os.environ["BUDTRA_DB_PASSW"])