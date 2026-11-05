from fastapi import APIRouter, HTTPException, status

from models.users import NewUser, UserSignIn


# Создаём маршрутизатор пользователей
user_router = APIRouter(
    tags=["User"]
)


# Временное хранилище пользователей
users = {}


# Регистрация пользователя
@user_router.post("/signup")
async def sign_new_user(data: NewUser) -> dict:

    email = str(data.email)

    # Проверяем, существует ли пользователь
    if email in users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with supplied email exists"
        )

    # Добавляем пользователя
    users[email] = data

    return {
        "message": "User successfully registered!"
    }


# Вход пользователя
@user_router.post("/signin")
async def sign_user_in(user: UserSignIn) -> dict:

    email = str(user.email)

    # Проверяем существование пользователя
    if email not in users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )

    # Проверяем правильность пароля
    if users[email].password != user.password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong credentials passed"
        )

    return {
        "message": "User signed in successfully"
    }
