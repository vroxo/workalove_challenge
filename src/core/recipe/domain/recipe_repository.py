from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from src.core.recipe.domain.recipe import Recipe


@dataclass
class SearchFilterRecipe:
    chef_name: Optional[str] = None
    name: Optional[str] = None
    ingredient: Optional[str] = None
    description: Optional[str] = None
    preparation_method: Optional[str] = None


class RecipeRepository(ABC):
    @abstractmethod
    def save(self, recipe: Recipe) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, recipe: Recipe) -> Recipe:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: UUID) -> Recipe:
        raise NotImplementedError

    @abstractmethod
    def search(self, filter: SearchFilterRecipe) -> list[Recipe]:
        raise NotImplementedError

    @abstractmethod
    def list_by_chef_id(self, chef_id: UUID) -> list[Recipe]:
        raise NotImplementedError
