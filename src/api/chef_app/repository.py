from uuid import UUID

from src.api.chef_app.models import ChefModel
from src.core.chef.domain.chef import Chef
from src.core.chef.domain.chef_repository import ChefRepository


class DjangoORMChefRepository(ChefRepository):
    def __init__(self, model: ChefModel | None = None) -> None:
        self.model = model or ChefModel

    def save(self, chef: Chef) -> None:
        chef_model = ChefModelMapper.to_model(chef)
        chef_model.save()

    def get_by_id(self, id: UUID) -> Chef | None:
        try:
            chef_model = self.model.objects.get(id=id)
            return ChefModelMapper.to_entity(chef_model)
        except self.model.DoesNotExist:
            return None


class ChefModelMapper:
    @staticmethod
    def to_entity(model: ChefModel) -> Chef:
        return Chef(
            id=model.id,
            name=model.name,
            is_active=model.is_active,
        )

    @staticmethod
    def to_model(entity: Chef) -> ChefModel:
        return ChefModel(
            id=entity.id,
            name=entity.name,
            is_active=entity.is_active,
        )
