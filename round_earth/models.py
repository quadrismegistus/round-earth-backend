from .imports import *
from .base import *


class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    posts: Mapped[List['Post']] = relationship(back_populates='user')

    @cached_property
    def places(self):
        return {post.place for post in self.posts}

    def __repr__(self):
        return f'User(id={self.id}, name={self.name})'


class Post(Base):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates='posts',
                                        foreign_keys=[user_id])

    place_id: Mapped[int] = mapped_column(ForeignKey("place.id"))
    place: Mapped["Place"] = relationship(foreign_keys=[place_id])

    text: Mapped[str]
    lang: Mapped[Optional[str]]

    translations: Mapped[List['Translation']] = relationship(
        back_populates='post')

    @classmethod
    def nearby(cls, lat, lon):
        point = get_point(lat, lon)
        for post in get_db_session().query(cls).join(Place).order_by(
                func.ST_Distance(
                    Place.point,
                    point,
                )):
            yield post, post.place.dist_from(lat, lon)

    def translate_to(self, lang):
        if lang == self.lang: return self
        transl = Translation.get(post_id=self.id, lang=lang)
        if not transl:
            res = translate_text(lang, self.text)
            transltext = res.get('translatedText')
            if transltext:
                transl = Translation(post_id=self.id,
                                     text=transltext,
                                     lang=lang).save()
        return transl

    def __repr__(self):
        return f'''
Post(
    id={self.id}, 
    text="{self.text}", 
    lang="{self.lang}", 
    user={self.user}, 
    place={self.place})'
)'''.strip()


class Translation(Base):
    __tablename__ = 'translation'
    id: Mapped[int] = mapped_column(primary_key=True)

    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))
    post: Mapped['Post'] = relationship(back_populates='translations',
                                        foreign_keys=[post_id])

    text: Mapped[str]
    lang: Mapped[str]

    def __repr__(self):
        return f'Translation(id={self.id}, post_id={self.post_id}, lang="{self.lang}", text="{self.text}")'


class Place(Base):
    __tablename__ = 'place'
    id: Mapped[int] = mapped_column(primary_key=True)
    point = Column(Geometry(geometry_type='POINT', srid=4326))
    name: Mapped[str]

    type: Mapped[Optional[str]]
    country: Mapped[Optional[str]] = mapped_column(String(2))

    @classmethod
    def nearby(cls, lat, lon):
        point = get_point(lat, lon)
        for place in get_db_session().query(cls).order_by(
                func.ST_Distance(
                    cls.point,
                    point,
                )):
            yield place, place.dist_from(lat, lon)

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

    @cached_property
    def point_str(self):
        return f'POINT({self.lon} {self.lat})'

    def __repr__(self):
        return f'Place(id={self.id}, name={self.name}, point="{self.point_str}")'


tables = [User, Place, Post, Translation]


def ensure_db_tables(clear=DB_CLEAR):
    if clear: clear_db()
    for table in tables:
        table.ensure_table()


def test():
    ensure_db_tables()
    user = User(name='Marx').save()
    place = Place(name='Trier', point='POINT(6.63935 49.75565)').save()
    post = Post(user_id=user.id,
                place_id=place.id,
                text='Guten morgen',
                lang='de').save()

    trans = Translation(post_id=post.id, text='Good morning', lang='en').save()

    return post
