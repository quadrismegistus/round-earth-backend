from .imports import *


def run():
    cmd = f'( cd "{PATH_REPO}" && uvicorn round_earth:app --reload )'
    os.system(cmd)


def get_spatialite_path():
    for path in PATHS_SPATIALITE:
        if os.path.exists(path):
            return path


def clear_db(db_url=None):
    if not db_url:
        db_url = f'postgresql://{DB_USERNAME}@{DB_HOST}/{DB_DATABASE}'
    if database_exists(db_url):
        cmd = f"psql -U {DB_USERNAME} -h {DB_HOST} -c 'DROP DATABASE {DB_DATABASE};'"
        os.system(cmd)


@cache
def get_db_engine(clear=DB_CLEAR):
    db_url = f'postgresql://{DB_USERNAME}@{DB_HOST}/{DB_DATABASE}'
    if clear:
        clear_db(db_url)

    if not database_exists(db_url):
        cmd1 = f"psql -U {DB_USERNAME} -h {DB_HOST} -c 'CREATE DATABASE {DB_DATABASE};'"
        cmd2 = f"psql -U {DB_USERNAME} -h {DB_HOST} -d {DB_DATABASE} -c 'CREATE EXTENSION postgis;'"
        os.system(f'{cmd1} && {cmd2}')

    return create_engine(db_url, echo=True)


@cache
def get_db_session():
    return Session(get_db_engine())


def get_point(lat, lon):
    pointstr = f'POINT({lon} {lat})'
    point = func.Geometry(func.ST_GeographyFromText(pointstr))
    return point
