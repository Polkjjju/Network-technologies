from fastapi import FastAPI
from todo import todo_router

app = FastAPI()


@app.get("/")
async def welcome() -> dict:
    return {"message": "Добро пожаловать в приложение FastAPI!"}


app.include_router(todo_router)
from fastapi import FastAPI
from todo import todo_router

app = FastAPI(
    title="Todo API",
    description="CRUD-приложение для управления задачами",
    version="1.0.0",
)


@app.get("/")
async def welcome() -> dict[str, str]:
    return {
        "message": "Добро пожаловать в Todo API!"
    }


app.include_router(todo_router)
