from .imports import *


class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    lang: str
    lat: float = Field(index=True)
    lon: float = Field(index=True)
    place_id: Optional[int] = Field(default=None, foreign_key="place.id")


class Place(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    lat: float
    lon: float
    name: str
    type: str
    country: str


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)


@cache
def get_db_engine():
    sqlite_file_name = os.path.join(PATH_DATA, "database.db")
    sqlite_url = f"sqlite:///{sqlite_file_name}"
    connect_args = {"check_same_thread": False}
    engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)
    return engine


def get_db_session():
    return Session(get_db_engine())


def create_db_and_tables():
    os.makedirs(PATH_DATA, exist_ok=True)
    SQLModel.metadata.create_all(get_db_engine())
