from sqlmodel import Session, SQLModel, create_engine
from models.todo import ToDo

engine = create_engine("sqlite:///todo.db", echo=True)
SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
