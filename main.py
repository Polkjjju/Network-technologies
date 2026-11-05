from fastapi import FastAPI

from routes.users import user_router
from routes.events import event_router


# Создаём приложение FastAPI
app = FastAPI(
    title="Planner API",
    description="Application for planning events",
    version="1.0.0"
)


# Подключаем маршруты пользователей
app.include_router(
    user_router,
    prefix="/user"
)


# Подключаем маршруты событий
app.include_router(
    event_router,
    prefix="/event"
)


# Запуск приложения
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8080,
        reload=True
    )
