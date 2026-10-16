
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Path,
    Request,
    status,
)
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from model import Todo


# Создание маршрутизатора
todo_router = APIRouter()

# Список задач
todo_list = []

# Подключение HTML-шаблонов
templates = Jinja2Templates(directory="templates")


# Получение списка задач
@todo_router.get("/todo")
async def retrieve_todo(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="todo.html",
        context={
            "todos": todo_list,
            "item": "",
        },
    )


# Добавление новой задачи
@todo_router.post("/todo")
async def add_todo(
    todo: Todo = Depends(Todo.as_form),
):
    # Назначение уникального ID
    todo.id = max(
        (task.id or 0 for task in todo_list),
        default=0,
    ) + 1

    todo_list.append(todo)

    # Возвращение к списку задач
    return RedirectResponse(
        url="/todo",
        status_code=status.HTTP_303_SEE_OTHER,
    )


# Удаление задачи
@todo_router.post("/todo/{todo_id}/delete")
async def delete_todo(
    todo_id: int = Path(..., title="ID задачи"),
):
    for index, todo in enumerate(todo_list):
        if todo.id == todo_id:
            # Удаляем задачу из списка
            todo_list.pop(index)

            # Перенаправляем пользователя к списку
            return RedirectResponse(
                url="/todo",
                status_code=status.HTTP_303_SEE_OTHER,
            )

    # Если задача не найдена
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Задача с указанным ID не найдена",
    )


# Просмотр одной задачи
@todo_router.get("/todo/{todo_id}")
async def get_single_todo(
    request: Request,
    todo_id: int = Path(..., title="ID задачи"),
):
    for todo in todo_list:
        if todo.id == todo_id:
            return templates.TemplateResponse(
                request=request,
                name="todo.html",
                context={
                    "todo": todo,
                    "item": "",
                },
            )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Задача с указанным ID не найдена",
    )
