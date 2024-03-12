from typing import List

from app import models
from app.repository.user import UserRepository


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def create_user(self, user: models.User) -> models.User:
        result = self.repository.add(user)
        return result

    def get_user(self, id: int) -> models.User:
        result = self.repository.get_by_id(id)
        return result

    def get_list_users(self) -> List[models.User]:
        result = self.repository.list()
        return result

    def update_user(self, id: int, user: models.User) -> models.User:
        result = self.repository.update(user)
        return result

    def delete_user(self, id: int) -> models.User:
        self.repository.delete(id)
