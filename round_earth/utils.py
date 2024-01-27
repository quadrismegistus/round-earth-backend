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


def translate_text(target: str, text: str) -> dict:
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    from google.cloud import translate_v2 as translate
    translate_client = translate.Client()
    if isinstance(text, bytes):
        text = text.decode("utf-8")
    result = translate_client.translate(text, target_language=target)
    return result


def geodecode(lat, lon):
    import reverse_geocode
    coords = (lat, lon)
    res = reverse_geocode.get(coords)
    return {
        'city': res.get('city', ''),
        'country': res.get('country_code', ''),
    }
