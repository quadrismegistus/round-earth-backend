from .imports import *
from .models import *

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


## users
@app.post("/users/")
def create_user(user: User):
    with get_db_session() as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


@app.get("/users/")
def read_users():
    with get_db_session() as session:
        users = session.exec(select(User)).all()
        return users


## places
@app.post("/places/")
def create_place(place: Place):
    with get_db_session() as session:
        session.add(place)
        session.commit()
        session.refresh(place)
        return place


@app.get("/places/")
def read_places():
    with get_db_session() as session:
        places = session.exec(select(Place)).all()
        return places


## posts


@app.post("/posts/")
def create_post(post: Post):
    with get_db_session() as session:
        session.add(post)
        session.commit()
        session.refresh(post)
        return post


@app.get("/posts/")
def read_posts():
    with get_db_session() as session:
        postes = session.exec(select(Post)).all()
        return postes
