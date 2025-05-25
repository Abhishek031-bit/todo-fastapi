from sqlmodel import Field, SQLModel


class ToDo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str
    completed: bool = False
