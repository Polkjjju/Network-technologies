from pydantic import BaseModel, ConfigDict


class Todo(BaseModel):
    id: int
    item: str
class TodoItem(BaseModel):
    item: str
class TodoItems(BaseModel):
    todos: list[TodoItem]
class TodoResponse(BaseModel):
    todo: Todo


class MessageResponse(BaseModel):
    message: str
from fastapi import APIRouter, HTTPException, Path, Query, status
from model import Todo, TodoItem, TodoItems, TodoResponse, MessageResponse
todo_router = APIRouter(tags=["Задачи"])

todo_list: list[Todo] = []
@todo_router.post(
    "/todo",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_todo(todo: Todo) -> MessageResponse:
    if any(existing.id == todo.id for existing in todo_list):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Задача с ID {todo.id} уже существует.",
        )

    todo_list.append(todo)

    return MessageResponse(
        message=f"Задача №{todo.id} успешно добавлена."
    )
@todo_router.get(
    "/todo",
    response_model=TodoItems,
)
async def retrieve_todos() -> TodoItems:
    return TodoItems(
        todos=[
            TodoItem(item=todo.item)
            for todo in todo_list
        ]
    )
@todo_router.get(
    "/todo/{todo_id}",
    response_model=TodoResponse,
)
async def get_single_todo(
    todo_id: int = Path(..., ge=1),
) -> TodoResponse:
    for todo in todo_list:
        if todo.id == todo_id:
            return TodoResponse(todo=todo)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Задача с ID {todo_id} не найдена.",
    )
@todo_router.put(
    "/todo/{todo_id}",
    response_model=MessageResponse,
)
async def update_todo(
    todo_data: TodoItem,
    todo_id: int = Path(..., ge=1),
) -> MessageResponse:
    for todo in todo_list:
        if todo.id == todo_id:
            todo.item = todo_data.item

            return MessageResponse(
                message=f"Задача №{todo_id} успешно обновлена."
            )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Задача с ID {todo_id} не найдена.",
    )
@todo_router.delete(
    "/todo/{todo_id}",
    response_model=MessageResponse,
)
async def delete_single_todo(
    todo_id: int = Path(..., ge=1),
) -> MessageResponse:
    for index, todo in enumerate(todo_list):
        if todo.id == todo_id:
            todo_list.pop(index)

            return MessageResponse(
                message=f"Задача №{todo_id} удалена."
            )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Задача с ID {todo_id} не найдена.",
    )
@todo_router.delete(
    "/todo",
    response_model=MessageResponse,
)
async def delete_all_todos() -> MessageResponse:
    todo_list.clear()

    return MessageResponse(
        message="Список задач очищен."
    )
@todo_router.get("/search")
async def search_todo(
    query: str = Query(..., min_length=1),
) -> dict[str, list[Todo]]:
    matches = [
        todo
        for todo in todo_list
        if query.casefold() in todo.item.casefold()
    ]

    return {"results": matches}
