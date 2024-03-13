from abc import ABC, abstractmethod
from typing import Callable

from sqlmodel import Session

from app.repository.user import UserRepository, UserReposityBase


class IUnitOfWork(ABC):
    user_repository: UserReposityBase

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_value:
            self.rollback()
        self.commit()

    @abstractmethod
    def commit(self):
        raise NotImplementedError()

    @abstractmethod
    def rollback(self):
        raise NotImplementedError()


class UnitOfWork(IUnitOfWork):
    def __init__(
        self,
        sql_session_factory: Callable[[], Session],
    ) -> None:
        self._sql_session_factory = sql_session_factory

    def __enter__(self):
        self._session: Session = self._sql_session_factory()
        self.user_repository = UserRepository(self._session)
        return super().__enter__()

    def commit(self):
        self._session.commit()

    def rollback(self):
        self._session.rollback()
