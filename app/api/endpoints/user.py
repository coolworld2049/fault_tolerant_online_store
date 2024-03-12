from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.responses import JSONResponse

from app import models
from app.api.deps import get_user_service
from app.service.user import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=models.User)
def create_user(
    user: models.User,
    user_service: UserService = Depends(get_user_service),
):
    user = user_service.create_user(user)
    return user


@router.get("/{id}", response_model=models.User)
def read_user(
    id: int,
    user_service: UserService = Depends(get_user_service),
):
    user = user_service.get_user(id)
    if user is None:
        raise HTTPException(status_code=404, detail="schemas.User not found")
    return user


@router.get("/", response_model=list[models.User])
def read_users(
    users_service: UserService = Depends(get_user_service),
):
    users = users_service.get_list_users()
    return users


@router.put("/{id}", response_model=models.User)
def update_user(
    id: int,
    user: models.UserUpdate,
    user_service: UserService = Depends(get_user_service),
):
    updated_user = user_service.update_user(
        id=id, user=models.User(**user.model_dump())
    )
    if updated_user is None:
        raise HTTPException(status_code=404, detail="schemas.User not found")
    return updated_user


@router.delete("/{id}", response_model=models.User)
def delete_user(
    id: int,
    user_service: UserService = Depends(get_user_service),
):
    user_service.delete_user(id)
    user = user_service.get_user(id)
    if user is None:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content="schemas.User already deleted"
        )
    return user