from fastapi import APIRouter, HTTPException, status
from typing import List

from models.events import Event


# Создаём маршрутизатор событий
event_router = APIRouter(
    tags=["Events"]
)


# Временное хранилище событий
events = []


# Получение всех событий
@event_router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:

    return events


# Получение одного события по ID
@event_router.get("/{event_id}", response_model=Event)
async def retrieve_event(event_id: int) -> Event:

    for event in events:
        if event.id == event_id:
            return event

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )


# Создание нового события
@event_router.post("/new")
async def create_event(body: Event) -> dict:

    # Проверяем уникальность ID
    for event in events:
        if event.id == body.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Event with supplied ID already exists"
            )

    events.append(body)

    return {
        "message": "Event created successfully"
    }


# Удаление одного события
@event_router.delete("/{event_id}")
async def delete_event(event_id: int) -> dict:

    for event in events:
        if event.id == event_id:
            events.remove(event)

            return {
                "message": "Event deleted successfully"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )


# Удаление всех событий
@event_router.delete("/")
async def delete_all_events() -> dict:

    events.clear()

    return {
        "message": "Events deleted successfully"
    }
