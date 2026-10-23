from fastapi import APIRouter, HTTPException, status

from models.events import Event


event_router = APIRouter(tags=["Events"])

# Временное хранилище событий
events: list[Event] = []


@event_router.get("/")
async def retrieve_all_events() -> list[Event]:
    return events


@event_router.get("/{id}")
async def retrieve_event(id: int) -> Event:
    for event in events:
        if event.id == id:
            return event

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )


@event_router.post("/new")
async def create_event(body: Event) -> dict:
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


@event_router.delete("/{id}")
async def delete_event(id: int) -> dict:
    for event in events:
        if event.id == id:
            events.remove(event)

            return {
                "message": "Event deleted successfully"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )


@event_router.delete("/")
async def delete_all_events() -> dict:
    events.clear()

    return {
        "message": "Events deleted successfully"
    }
