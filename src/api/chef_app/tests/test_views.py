from uuid import UUID

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from src.api.chef_app.repository import DjangoORMChefRepository
from src.core.chef.domain.chef import Chef


@pytest.fixture
def repository():
    return DjangoORMChefRepository()


@pytest.mark.django_db
def test_when_request_data_is_valid_then_create_category(repository) -> None:
    url = reverse('chefs-list')
    data = {
        'name': 'Chef',
    }
    response = APIClient().post(url, data=data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['id']

    saved_chef = repository.get_by_id(response.data['id'])
    assert repr(saved_chef) == repr(
        Chef(
            id=UUID(response.data['id']),
            name='Chef',
            is_active=True,
        )
    )


def test_when_request_data_is_invalid_then_return_400() -> None:
    url = reverse('chefs-list')
    data = {
        'name': '',
    }
    response = APIClient().post(url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {'name': ['This field may not be blank.']}
