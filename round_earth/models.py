from .imports import *

Base = declarative_base()


def save(self):
    self.ensure_table()
    db = get_db_session()
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


class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    # posts: Mapped[List['Post']] = relationship(back_populates='user')


class Post(Base):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(foreign_keys=[user_id])

    place_id: Mapped[int] = mapped_column(ForeignKey("place.id"))
    place: Mapped["Place"] = relationship(foreign_keys=[place_id])

    text: Mapped[str]
    lang: Mapped[Optional[str]]

    @classmethod
    def query_by_dist(cls, lat, lon):
        pointstr = f'POINT({lon} {lat})'
        point = func.Geometry(func.ST_GeographyFromText(pointstr))
        return get_db_session().query(cls).join(Place).order_by(
            func.ST_Distance(
                Place.point,
                point,
            ))

    def dist_from(self, *x, **y):
        return self.place.dist_from(*x, **y)


class Translation(Base):
    __tablename__ = 'translation'
    id: Mapped[int] = mapped_column(primary_key=True)

    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))
    post: Mapped['Post'] = relationship()

    text: Mapped[str]
    lang: Mapped[str]


class Place(Base):
    __tablename__ = 'place'
    id: Mapped[int] = mapped_column(primary_key=True)
    point = Column(Geometry(geometry_type='POINT', srid=4326))
    name: Mapped[str]

    type: Mapped[Optional[str]]
    country: Mapped[Optional[str]] = mapped_column(String(2))

    @classmethod
    def query_by_dist(cls, lat, lon):
        point = get_point(lat, lon)
        return get_db_session().query(cls).order_by(
            func.ST_Distance(
                cls.point,
                point,
            ))

    def dist_from(self, lat, lon, metric='km'):
        dist = geodesic((lon, lat), (self.lon, self.lat))
        return getattr(dist, metric)

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


tables = [User, Place, Post, Translation]


def ensure_db_tables():
    for table in tables:
        table.ensure_table()


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
