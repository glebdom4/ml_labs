import sqlite3
import sys
import os
import traceback

from tqdm import tqdm
from requests.exceptions import RequestException
from contextlib import closing
from ..vacancies import get_vacancy
from ..constants import DB_FILE_PATH
from ..constants import SHEMA_FILE_PATH
from ..constants import INSERT_FILE_PATH
from ..constants import DOWNLOADING_VACANCIES_MSG


def create_db(db_file=DB_FILE_PATH):
    """
    Creates a SQLite database.
    """
    try:
        with sqlite3.connect(db_file) as db:
            with open(SHEMA_FILE_PATH, 'r') as f, closing(db.cursor()) as cur:
                cur.executescript(f.read())
        return True
    except sqlite3.Error as err:
        print(err, file=sys.stderr)
        traceback.print_stack()
    except IOError as err:
        print(err, file=sys.stderr)
    return False


def save_vacancy(vacancy, connection_obj):
    """
    Saves a vacancy to the SQLite database.
    """
    try:
        with open(INSERT_FILE_PATH, 'r') as f, closing(connection_obj.cursor()) as cur:
            # saving area
            cur.execute(f.readline(),
                        (int(vacancy['area']['id']),
                        vacancy['area']['url'],
                        vacancy['area']['name']))
            # saving salary
            cur.execute(f.readline(),
                        (vacancy['salary']['from'],
                        vacancy['salary']['to'],
                        vacancy['salary']['currency'],
                        vacancy['salary']['gross']))
            cur.execute(f.readline())
            salaryID = cur.fetchone()[0]
            # saving employer
            cur.execute(f.readline(),
                       (vacancy['employer'].get('id', 'NULL'),
                        vacancy['employer']['name'],
                        vacancy['employer'].get('url', 'NULL'),
                        vacancy['employer'].get('alternate_url', 'NULL'),
                        vacancy['employer'].get('trusted', 'NULL'),
                        vacancy['employer'].get('blacklisted', 'NULL')))
            cur.execute(f.readline())
            employerID = cur.fetchone()[0]
            # saving vacancy
            cur.execute(f.readline(),
                        (int(vacancy['id']),
                        vacancy['name'],
                        vacancy['description'],
                        vacancy['published_at'],
                        int(vacancy['area']['id']),
                        salaryID,
                        employerID))
            connection_obj.commit()
    except IOError as err:
        print(err, file=sys.stderr)


def vacancies_to_db(id_list, db_file=DB_FILE_PATH, recreate=False):
    """
    Saves vacancies which IDs are transferred in the list
    to the SQLite database.
    """
    if recreate or not os.path.exists(db_file):
        create_db(db_file)
    try:
        with sqlite3.connect(db_file) as db:
            print(DOWNLOADING_VACANCIES_MSG)
            for vac_id in tqdm(id_list):
                vac = get_vacancy(vac_id)
                save_vacancy(vac, db)
        return True
    except RequestException as err:
        print(err, file=sys.stderr)
    except sqlite3.Error as err:
        print(err, file=sys.stderr)
        traceback.print_stack()
    return False
