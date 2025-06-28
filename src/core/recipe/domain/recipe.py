from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from src.core.shared.domain.entity import Entity

MAX_LENGTH = 255


@dataclass(eq=False)
class Recipe(Entity):
    chef_id: UUID
    name: str
    ingredients: list[str]
    preparation_method: str
    description: Optional[str] = None
    is_active: bool = True

    def __post_init__(self):
        self.validate()

    def validate(self):
        if not self.chef_id:
            self.notification.add_error('chef_id cannot be none')

        if len(self.name) > MAX_LENGTH:
            self.notification.add_error('name cannot be longer than 255')

        if self.description and len(self.description) > MAX_LENGTH:
            self.notification.add_error('description cannot be longer than 255')

        if not self.name:
            self.notification.add_error('name cannot be empty')

        if not self.preparation_method:
            self.notification.add_error('preparation_method cannot be empty')

        if not self.ingredients or len(self.ingredients) == 0:
            self.notification.add_error('ingredients cannot be empty')

        if self.notification.has_errors:
            raise ValueError(self.notification.messages)

    def update(self, name: str, description: str, ingredients: list[str], preparation_method: str):
        self.name = name
        self.description = description
        self.ingredients = ingredients
        self.preparation_method = preparation_method

        self.validate()

    def activate(self):
        self.is_active = True
        self.validate()

    def deactivate(self):
        self.is_active = False
        self.validate()
