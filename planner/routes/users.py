from fastapi import APIRouter, HTTPException, status

from models.users import NewUser, UserSignIn


user_router = APIRouter(tags=["User"])

# Временное хранилище пользователей
users: dict[str, NewUser] = {}


@user_router.post("/signup")
async def sign_new_user(data: NewUser) -> dict:
    email = str(data.email)

    if email in users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with supplied email exists"
        )

    users[email] = data

    return {
        "message": "User successfully registered!"
    }


@user_router.post("/signin")
async def sign_user_in(user: UserSignIn) -> dict:
    email = str(user.email)
    registered_user = users.get(email)

    if registered_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )

    if registered_user.password != user.password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong credentials passed"
        )

    return {
        "message": "User signed in successfully"
    }
