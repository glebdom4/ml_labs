import os


# requests constants
URL_API_VACANCIES = 'https://api.hh.ru/vacancies'

# sqlite3 constants
cur_dir = os.path.abspath(os.path.dirname(__file__))

DB_FILE_NAME = 'vacancies.db'
DB_FILE_PATH = os.path.join(cur_dir, 'data', DB_FILE_NAME)

SHEMA_FILE_NAME = 'schema.sql'
SHEMA_FILE_PATH = os.path.join(cur_dir, 'sql',
                               'db_creation_files', SHEMA_FILE_NAME)

INSERT_FILE_NAME = 'insert_vacancy.sql'
INSERT_FILE_PATH = os.path.join(cur_dir, 'sql',
                                'db_creation_files', INSERT_FILE_NAME)

# messages constants

GETTING_IDS_MSG = ("Getting the list of vacancies'IDs "
                   "issued by the search query.\n"
                   "Reading pages:")
DOWNLOADING_VACANCIES_MSG = "Downloading and saving vacancies:"
