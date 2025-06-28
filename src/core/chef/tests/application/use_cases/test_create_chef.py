from unittest.mock import create_autospec

import pytest

from src.core.chef.application.use_cases.create_chef import CreateChef
from src.core.chef.application.use_cases.exceptions import InvalidChef
from src.core.chef.domain.chef import Chef
from src.core.chef.domain.chef_repository import ChefRepository


@pytest.fixture
def mock_repository():
    return create_autospec(ChefRepository)


@pytest.fixture
def use_case(mock_repository):
    return CreateChef(repository=mock_repository)


def test_must_be_able_to_create_chef_with_valid_data(mock_repository, use_case):
    input = CreateChef.Input(name='Test Chef', is_active=True)
    output = use_case.execute(input)

    assert output == CreateChef.Output(id=output.id)

    chef = Chef(id=output.id, name=input.name, is_active=input.is_active)

    mock_repository.save.assert_called_once_with(chef)


def test_should_be_able_to_raises_invalid_chef_when_provided_invalid_data(use_case):
    input = CreateChef.Input(name=256 * 'a', is_active=True)
    with pytest.raises(InvalidChef, match='name cannot be longer than 255'):
        use_case.execute(input=input)

    input = CreateChef.Input(name='', is_active=True)
    with pytest.raises(InvalidChef, match='name cannot be empty'):
        use_case.execute(input=input)
