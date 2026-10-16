
from fastapi import APIRouter, HTTPException, Path, Query, status
from model import Todo, TodoItem, TodoItems, TodoResponse, MessageResponse

todo_router = APIRouter(tags=["Задачи"])

todo_list = []


@todo_router.post("/todo", status_code=status.HTTP_201_CREATED)
async def add_todo(todo: Todo) -> MessageResponse:
    for existing_todo in todo_list:
        if existing_todo.id == todo.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Задача с ID {todo.id} уже существует."
            )

    todo_list.append(todo)
    return MessageResponse(message="Задача успешно добавлена.")


@todo_router.get("/todo", response_model=TodoItems)
async def retrieve_todos() -> TodoItems:
    return TodoItems(
        todos=[TodoItem(item=todo.item) for todo in todo_list]
    )


@todo_router.get("/todo/{todo_id}", response_model=TodoResponse)
async def get_single_todo(
    todo_id: int = Path(..., title="ID задачи", ge=1)
) -> TodoResponse:
    for todo in todo_list:
        if todo.id == todo_id:
            return TodoResponse(todo=todo)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Задача с ID {todo_id} не найдена."
    )


@todo_router.put(
    "/todo/{todo_id}",
    response_model=MessageResponse
)
async def update_todo(
    todo_data: TodoItem,
    todo_id: int = Path(..., ge=1)
) -> MessageResponse:
    for todo in todo_list:
        if todo.id == todo_id:
            todo.item = todo_data.item
            return MessageResponse(
                message=f"Задача №{todo_id} успешно обновлена."
            )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Задача с ID {todo_id} не найдена."
    )


@todo_router.delete(
    "/todo/{todo_id}",
    response_model=MessageResponse
)
async def delete_single_todo(
    todo_id: int = Path(..., ge=1)
) -> MessageResponse:
    for index, todo in enumerate(todo_list):
        if todo.id == todo_id:
            todo_list.pop(index)
            return MessageResponse(
                message=f"Задача №{todo_id} успешно удалена."
            )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Задача с ID {todo_id} не найдена."
    )


@todo_router.delete("/todo", response_model=MessageResponse)
async def delete_all_todos() -> MessageResponse:
    todo_list.clear()
    return MessageResponse(message="Все задачи удалены.")


@todo_router.get("/search")
async def search_todo(query: str = Query(None)) -> dict:
    results = [
        todo for todo in todo_list
        if query and query.lower() in todo.item.lower()
    ]
    return {"results": results}
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Path,
    Request,
    status,
)
from fastapi.templating import Jinja2Templates

from model import Todo


todo_router = APIRouter()

todo_list = []

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
    request: Request,
    todo: Todo = Depends(Todo.as_form),
):
    todo.id = len(todo_list) + 1
    todo_list.append(todo)

    return templates.TemplateResponse(
        request=request,
        name="todo.html",
        context={
            "todos": todo_list,
            "item": "",
        },
    )


# Получение одной задачи
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
