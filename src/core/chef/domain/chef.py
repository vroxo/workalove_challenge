from dataclasses import dataclass

from src.core.shared.domain.entity import Entity

MAX_LENGTH_NAME = 255


@dataclass(eq=False)
class Chef(Entity):
    name: str
    is_active: bool = True

    def __post_init__(self):
        self.validate()

    def validate(self):
        if len(self.name) > MAX_LENGTH_NAME:
            self.notification.add_error('name cannot be longer than 255')

        if not self.name:
            self.notification.add_error('name cannot be empty')

        if self.notification.has_errors:
            raise ValueError(self.notification.messages)

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'<Chef {self.id} {self.name}>'

    def update(self, name: str):
        self.name = name
        self.validate()

    def activate(self):
        self.is_active = True
        self.validate()

    def deactivate(self):
        self.is_active = False
        self.validate()
