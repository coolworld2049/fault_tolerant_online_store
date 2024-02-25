from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.responses import JSONResponse

from app import schemas
from app.api.deps import get_user_service
from app.schemas import User
from app.service.user import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=schemas.User)
def create_user(
    user: User,
    user_service: UserService = Depends(get_user_service),
):
    user = user_service.create_user(user)
    return user


@router.get("/{id}", response_model=schemas.User)
def read_user(
    id: int,
    user_service: UserService = Depends(get_user_service),
):
    user = user_service.get_user(id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=list[schemas.User])
def read_users(
    users_service: UserService = Depends(get_user_service),
):
    users = users_service.get_list_users()
    return users


@router.put("/{id}", response_model=schemas.User)
def update_user(
    user: User,
    user_service: UserService = Depends(get_user_service),
):
    updated_user = user_service.update_user(user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.delete("/{id}", response_model=schemas.User)
def delete_user(
    id: int,
    user_service: UserService = Depends(get_user_service),
):
    user_service.delete_user(id)
    user = user_service.get_user(id)
    if user is None:
        return JSONResponse(status_code=status.HTTP_200_OK, content="User already deleted")
    return user
