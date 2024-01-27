from .imports import *

Base = declarative_base()


def save(self):
    self.ensure_table()
    db = get_db_session()
    db.add(self)
    db.commit()
    return self


@classmethod
def query_by_attr(cls, **kwargs):
    assert kwargs
    key, val = list(kwargs.items())[0]
    db = get_db_session()
    return db.query(cls).filter(getattr(cls, key) == val)


@classmethod
def get(cls, **kwargs):
    return cls.query_by_attr(**kwargs).first()


@classmethod
def find(cls, **kwargs):
    return cls.query_by_attr(**kwargs).all()


@classmethod
def ensure_table(self):
    engine = get_db_engine()
    with engine.connect() as conn:
        if not engine.dialect.has_table(conn, self.__tablename__):
            self.__table__.create(engine)


Base.save = save
Base.query_by_attr = query_by_attr
Base.get = get
Base.find = find
Base.ensure_table = ensure_table
