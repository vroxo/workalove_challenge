from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from src.core.shared.domain.notification import Notification


@dataclass(kw_only=True, eq=False)
class Entity(ABC):
    id: UUID = field(default_factory=uuid4)
    notification: Notification = field(default_factory=Notification)
    created_at: datetime = field(default_factory=datetime.now, init=False)
    updated_at: datetime = field(default_factory=datetime.now, init=False)

    def __eq__(self, other: 'Entity'):
        if not isinstance(other, self.__class__):
            return False

        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    @abstractmethod
    def validate(self):
        pass
