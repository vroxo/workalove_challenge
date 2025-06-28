from abc import ABC, abstractmethod
from uuid import UUID

from src.core.chef.domain.chef import Chef


class ChefRepository(ABC):
    @abstractmethod
    def save(self, chef: Chef) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: UUID) -> Chef | None:
        raise NotImplementedError
