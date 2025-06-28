from urllib.parse import urlencode
from uuid import uuid4

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from src.api.recipe_app.repository import DjangoORMRecipeRepository


@pytest.fixture
def repository():
    return DjangoORMRecipeRepository()


@pytest.mark.django_db
def test_when_request_data_is_valid_then_create_recipe() -> None:
    chefs_url = reverse('chefs-list')
    chef_data = {
        'name': 'Chef',
    }
    chefs_response = APIClient().post(chefs_url, data=chef_data)
    chef_id = chefs_response.data['id']

    url = reverse('recipes-list')
    data = {
        'chef_id': chef_id,
        'name': 'Brigadeiro',
        'description': 'Receita de Brigadeiro',
        'ingredients': [
            '1 Lata de Leite Condensado',
            '2 Colheres de Sopa de Achocolatado',
            '1 Colher de Chá de Manteiga',
        ],
        'preparation_method': 'Misture tudo e leve al fogo médio até pegar o ponto',
    }

    response = APIClient().post(url, data=data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['id']


def test_when_create_recipe_request_data_is_invalid_then_return_400() -> None:
    url = reverse('recipes-list')
    data = {
        'name': 'Brigadeiro',
        'ingredients': [
            '1 Lata de Leite Condensado',
            '2 Colheres de Sopa de Achocolatado',
            '1 Colher de Chá de Manteiga',
        ],
        'preparation_method': 'Misture tudo e leve al fogo médio até pegar o ponto',
    }

    response = APIClient().post(url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {'chef_id': ['This field is required.']}


@pytest.mark.django_db
def test_when_create_recipe_request_provided_chef_id_not_found_then_return_404() -> None:
    url = reverse('recipes-list')
    data = {
        'chef_id': str(uuid4()),
        'name': 'Brigadeiro',
        'ingredients': [
            '1 Lata de Leite Condensado',
            '2 Colheres de Sopa de Achocolatado',
            '1 Colher de Chá de Manteiga',
        ],
        'preparation_method': 'Misture tudo e leve al fogo médio até pegar o ponto',
    }

    response = APIClient().post(url, data=data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data == {'detail': 'chef not found'}


@pytest.mark.django_db
def test_when_request_data_is_valid_then_update_recipe() -> None:
    chefs_url = reverse('chefs-list')
    chef_data = {
        'name': 'Chef',
    }
    chefs_response = APIClient().post(chefs_url, data=chef_data)
    chef_id = chefs_response.data['id']

    create_url = reverse('recipes-list')
    create_data = {
        'chef_id': chef_id,
        'name': 'Brigadeiro',
        'description': 'Receita de Brigadeiro',
        'ingredients': [
            '1 Lata de Leite Condensado',
            '2 Colheres de Sopa de Achocolatado',
            '1 Colher de Chá de Manteiga',
        ],
        'preparation_method': 'Misture tudo e leve al fogo médio até pegar o ponto',
    }

    create_response = APIClient().post(create_url, data=create_data)

    url = reverse('recipes-detail', kwargs={'pk': create_response.data['id']})
    data = {
        'name': 'Updated Brigadeiro',
        'description': 'Updated Receita de Brigadeiro',
    }

    response = APIClient().put(url, data=data, format='json')

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_when_recipe_exists_then_delete_recipe() -> None:
    chefs_url = reverse('chefs-list')
    chef_data = {
        'name': 'Chef',
    }
    chefs_response = APIClient().post(chefs_url, data=chef_data)
    chef_id = chefs_response.data['id']

    create_url = reverse('recipes-list')
    create_data = {
        'chef_id': chef_id,
        'name': 'Brigadeiro',
        'description': 'Receita de Brigadeiro',
        'ingredients': [
            '1 Lata de Leite Condensado',
            '2 Colheres de Sopa de Achocolatado',
            '1 Colher de Chá de Manteiga',
        ],
        'preparation_method': 'Misture tudo e leve al fogo médio até pegar o ponto',
    }

    create_response = APIClient().post(create_url, data=create_data)

    url = reverse('recipes-detail', kwargs={'pk': create_response.data['id']})

    response = APIClient().delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_when_search_recipes_exists() -> None:
    chefs_url = reverse('chefs-list')
    chef_data = {
        'name': 'Chef',
    }
    chefs_response = APIClient().post(chefs_url, data=chef_data)
    chef_id = chefs_response.data['id']

    create_url = reverse('recipes-list')
    create_data = {
        'chef_id': chef_id,
        'name': 'Brigadeiro',
        'description': 'Receita de Brigadeiro',
        'ingredients': [
            '1 Lata de Leite Condensado',
            '2 Colheres de Sopa de Achocolatado',
            '1 Colher de Chá de Manteiga',
        ],
        'preparation_method': 'Misture tudo e leve al fogo médio até pegar o ponto',
    }

    APIClient().post(create_url, data=create_data)

    url = reverse('recipes-search')
    params = {'chef_name': 'chef', 'name': 'brigadeiro'}
    url_with_params = f'{url}?{urlencode(params)}'

    response = APIClient().get(url_with_params)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['data']) == 1

    params = {'chef_name': 'chef', 'name': 'brigadeiro', 'ingredient': 'ovo'}
    url_with_params = f'{url}?{urlencode(params)}'

    response = APIClient().get(url_with_params)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['data']) == 0


@pytest.mark.django_db
def test_when_list_recipes_by_chef() -> None:
    chefs_url = reverse('chefs-list')
    chef_data = {
        'name': 'Chef',
    }
    chefs_response = APIClient().post(chefs_url, data=chef_data)
    chef_id = chefs_response.data['id']

    create_url = reverse('recipes-list')
    create_data = {
        'chef_id': chef_id,
        'name': 'Brigadeiro',
        'description': 'Receita de Brigadeiro',
        'ingredients': [
            '1 Lata de Leite Condensado',
            '2 Colheres de Sopa de Achocolatado',
            '1 Colher de Chá de Manteiga',
        ],
        'preparation_method': 'Misture tudo e leve al fogo médio até pegar o ponto',
    }

    APIClient().post(create_url, data=create_data)

    url = reverse('recipes-by-chef', kwargs={'chef_id': chef_id})

    response = APIClient().get(url)

    assert len(response.data['data']) == 1
