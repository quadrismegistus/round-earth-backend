from .imports import *
from .models import *

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/posts/")
def create_post(post: Post):
    with get_db_session() as session:
        session.add(post)
        session.commit()
        session.refresh(post)
        return post


@app.get("/postes/")
def read_postes():
    with get_db_session() as session:
        postes = session.exec(select(Post)).all()
        return postes
