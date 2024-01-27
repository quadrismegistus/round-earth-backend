from .imports import *


class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    place_id: Optional[int] = Field(default=None, foreign_key="place.id")
    text_id: Optional[int] = Field(default=None, foreign_key="text.id")


class Text(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    lang: Optional[str] = ''


class Translation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text_id: Optional[int] = Field(default=None, foreign_key="text.id")
    text: str
    lang: str


class Place(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    point: Any = Field(sa_column=Column(Geometry('POINT')))
    name: str
    type: Optional[str] = ''
    country: Optional[str] = ''


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)


@cache
def get_db_engine(clear=True):
    sqlite_file_name = os.path.join(PATH_DATA, "database.db")
    if clear and os.path.exists(sqlite_file_name):
        os.unlink(sqlite_file_name)

    sqlite_url = f"sqlite:///{sqlite_file_name}"
    connect_args = {"check_same_thread": False}
    engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

    spatialite_path = get_spatialite_path()
    if spatialite_path:
        os.environ['SPATIALITE_LIBRARY_PATH'] = spatialite_path
        listen(engine, "connect", load_spatialite)
    return engine


def get_db_session():
    return Session(get_db_engine())


def create_db_and_tables():
    os.makedirs(PATH_DATA, exist_ok=True)
    SQLModel.metadata.create_all(get_db_engine())
