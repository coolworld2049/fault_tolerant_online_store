from fastapi.params import Depends
from starlette.requests import Request

from app.repository.user import UserRepository
from app.service.unit_of_work import UnitOfWork
from app.service.user import UserService


def get_user_repository(requset: Request):
    sql_session_factory = requset.app.state.sql_session_factory
    with UnitOfWork(session_factory=sql_session_factory) as uow:
        try:
            yield uow.users
        except:  # noqa
            uow.rollback()
        finally:
            uow.commit()


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(user_repository)
