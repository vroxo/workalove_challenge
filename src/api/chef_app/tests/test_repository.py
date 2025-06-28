from uuid import uuid4

import pytest

from src.api.chef_app.models import ChefModel
from src.api.chef_app.repository import DjangoORMChefRepository
from src.core.chef.domain.chef import Chef


@pytest.mark.django_db
def test_saves_chef_in_database():
    chef = Chef(
        name='Test Chef',
    )
    repository = DjangoORMChefRepository()

    assert ChefModel.objects.count() == 0
    repository.save(chef)
    assert ChefModel.objects.count() == 1
    saved_chef = ChefModel.objects.get()

    assert saved_chef.id == chef.id
    assert saved_chef.name == chef.name
    assert saved_chef.is_active == chef.is_active


@pytest.mark.django_db
def test_get_chef_by_id_from_database():
    chef = Chef(
        name='Test Chef',
    )
    repository = DjangoORMChefRepository()
    repository.save(chef)

    assert ChefModel.objects.count() == 1
    saved_chef = repository.get_by_id(chef.id)

    assert saved_chef.id == chef.id
    assert saved_chef.name == chef.name
    assert saved_chef.is_active == chef.is_active


@pytest.mark.django_db
def test_get_chef_by_id_from_database_when_not_exists():
    repository = DjangoORMChefRepository()
    saved_chef = repository.get_by_id(uuid4())

    assert saved_chef is None
