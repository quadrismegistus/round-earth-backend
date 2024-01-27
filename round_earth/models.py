from .imports import *

Base = declarative_base()


def save(self):
    self.ensure_table()
    with get_db_session() as db:
        db.add(self)
        db.commit()
    return self


@classmethod
def ensure_table(self):
    engine = get_db_engine()
    with engine.connect() as conn:
        if not engine.dialect.has_table(conn, self.__tablename__):
            self.__table__.create(engine)


Base.save = save
Base.ensure_table = ensure_table

# class Post(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     user_id: Optional[int] = Field(default=None, foreign_key="user.id")
#     place_id: Optional[int] = Field(default=None, foreign_key="place.id")
#     text_id: Optional[int] = Field(default=None, foreign_key="text.id")

# class Text(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     text: str
#     lang: Optional[str] = ''

# class Translation(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     text_id: Optional[int] = Field(default=None, foreign_key="text.id")
#     text: str
#     lang: str


class Place(Base):
    __tablename__ = 'place'
    id = Column(Integer, primary_key=True)
    point = Column(Geometry(geometry_type='POINT', srid=4326))
    name = Column(String)
    type = Column(String, nullable=True, default='')
    country = Column(String, nullable=True, default='')

    @classmethod
    def query_by_dist(cls, lat, lon):
        pointstr = f'POINT({lon} {lat})'
        point = func.Geometry(func.ST_GeographyFromText(pointstr))
        with get_db_session() as db:
            for res in db.query(cls).order_by(
                    func.ST_Distance(cls.point, point)):
                yield res
                # res.distance = geodesic((lat, lon), (res.lat, res.lon))
                # yield res

    @cached_property
    def latlon(self):
        point = wkb.loads(self.point.data.tobytes())
        return (point.y, point.x)

    @property
    def lat(self):
        return self.latlon[0]

    @property
    def lon(self):
        return self.latlon[1]


# class User(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     name: str = Field(index=True)

# @cache
# def get_db_engine(clear=True):
#     return create_engine('postgresql://localhost/round_earth', echo=True)

# def get_db_session():
#     return Session(get_db_engine())

# def create_db_and_tables():
#     os.makedirs(PATH_DATA, exist_ok=True)
#     SQLModel.metadata.create_all(get_db_engine())
