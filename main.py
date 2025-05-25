from typing import Sequence

from database.db import get_session
from fastapi import Depends, FastAPI, HTTPException
from models.todo import ToDo
from sqlmodel import Session, select

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Welcome to todo-fastapi"}


@app.post("/todo", response_model=ToDo)
def create_todo(todo: ToDo, session: Session = Depends(get_session)) -> dict[str, str]:
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return {"message": "Successfully created todo"}


@app.get("/todo", response_model=list[ToDo])
def get_all_todos(session: Session = Depends(get_session)) -> Sequence[ToDo]:
    return session.exec(select(ToDo)).all()


@app.get("/todo/{id}")
def get_todo_by_id(id: int, session: Session = Depends(get_session)):
    todo: ToDo | None = session.get(ToDo, id)
    if todo:
        return todo
    return HTTPException(status_code=404, detail="Todo not found")


@app.put("/todo/{id}")
def toggle_todo(id: int, session: Session = Depends(get_session)):
    todo: ToDo | None = session.get(ToDo, id)
    if todo:
        todo.completed = not todo.completed
        session.add(todo)
        session.commit()
        return {"message": "Successfully updated todo"}
    return HTTPException(status_code=404, detail="Todo not found")


@app.delete("/todo/{id}")
def delete_todo(id: int, session: Session = Depends(get_session)):
    todo: ToDo | None = session.get(ToDo, id)
    if todo:
        session.delete(todo)
        session.commit()
        return {"message": "Successfully deleted todo"}
    return HTTPException(status_code=404, detail="Todo not found")


if __name__ == "__main__":
    import uvicorn

    # Set host to 0.0.0.0 to allow connections from render
    uvicorn.run("main:app", host="0.0.0.0")
