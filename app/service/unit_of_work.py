from abc import ABC, abstractmethod
from typing import Callable

from sqlmodel import Session

from app.repository.user import UserRepository, UserReposityBase


class IUnitOfWork(ABC):
    users: UserReposityBase

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.rollback()

    @abstractmethod
    def commit(self):
        raise NotImplementedError()

    @abstractmethod
    def rollback(self):
        raise NotImplementedError()


class UnitOfWork(IUnitOfWork):
    def __init__(
        self,
        session_factory: Callable[[], Session],
    ) -> None:
        self._session_factory = session_factory

    def __enter__(self):
        self._session: Session = self._session_factory()
        self.users = UserRepository(self._session)
        return super().__enter__()

    def commit(self):
        self._session.commit()

    def rollback(self):
        self._session.rollback()
