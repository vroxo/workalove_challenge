from dataclasses import asdict, dataclass
from uuid import UUID

from src.core.chef.application.use_cases.exceptions import InvalidChef
from src.core.chef.domain.chef import Chef
from src.core.chef.domain.chef_repository import ChefRepository


class CreateChef:
    def __init__(self, repository: ChefRepository):
        self.repository = repository

    @dataclass
    class Input:
        name: str
        is_active: bool

    @dataclass
    class Output:
        id: UUID

    def execute(self, input: Input) -> Output:
        try:
            chef = Chef(**asdict(input))
            self.repository.save(chef)
            return CreateChef.Output(id=chef.id)
        except ValueError as error:
            raise InvalidChef(error)
