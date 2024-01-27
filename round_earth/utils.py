from .imports import *


def run():
    cmd = f'( cd "{PATH_REPO}" && uvicorn round_earth:app --reload )'
    os.system(cmd)


def get_spatialite_path():
    for path in PATHS_SPATIALITE:
        if os.path.exists(path):
            return path


@cache
def get_db_engine(clear=True):
    db_url = f'postgresql://{DB_USERNAME}@{DB_HOST}/{DB_DATABASE}'
    if clear and database_exists(db_url):
        cmd = f"psql -U {DB_USERNAME} -h {DB_HOST} -c 'DROP DATABASE {DB_DATABASE};'"
        os.system(cmd)

    if not database_exists(db_url):
        cmd1 = f"psql -U {DB_USERNAME} -h {DB_HOST} -c 'CREATE DATABASE {DB_DATABASE};'"
        cmd2 = f"psql -U {DB_USERNAME} -h {DB_HOST} -d {DB_DATABASE} -c 'CREATE EXTENSION postgis;'"
        os.system(f'{cmd1} && {cmd2}')

    return create_engine(db_url, echo=True)


def get_db_session():
    return Session(get_db_engine())
