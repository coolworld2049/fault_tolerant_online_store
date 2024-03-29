from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy.exc import SQLAlchemyError
from starlette import status
from starlette.requests import Request

from app.repository.user import UserRepository
from app.uow.uow import UnitOfWork
from app.service.user import UserService


def get_user_repository(requset: Request):
    sql_session_factory = requset.app.state.sql_session_factory
    try:
        with UnitOfWork(session_factory=sql_session_factory) as uow:
            yield uow.user_repository
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.orig.__class__.__name__
        )


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    yield UserService(user_repository)
