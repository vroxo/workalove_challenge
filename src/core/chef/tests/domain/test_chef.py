from uuid import UUID, uuid4

import pytest

from src.core.chef.domain.chef import Chef


def test_must_be_able_to_create_chef_with_valid_data():
    chef = Chef(name='Test Chef', is_active=True)

    assert isinstance(chef.id, UUID)
    assert chef.name == 'Test Chef'
    assert chef.is_active is True


def test_should_be_able_to_raises_value_error_when_invalid_data():
    with pytest.raises(ValueError, match='name cannot be longer than 255'):
        Chef(name=256 * 'a', is_active=True)

    with pytest.raises(ValueError, match='name cannot be empty'):
        Chef(name='', is_active=True)


def test_should_be_able_to_update_chef_with_valid_name():
    chef = Chef(name='Test Chef', is_active=True)

    chef.update('Updated Chef')

    assert chef.name == 'Updated Chef'


def test_should_be_able_to_raises_value_error_when_invalid_name():
    chef = Chef(name='Test Chef', is_active=True)

    with pytest.raises(ValueError, match='name cannot be longer than 255'):
        chef.update(256 * 'a')

    with pytest.raises(ValueError, match='name cannot be empty'):
        chef.update('')


def test_should_be_able_to_activate_chef_when_is_deactivated():
    chef = Chef(name='Test Chef', is_active=False)
    chef.activate()

    assert chef.is_active is True


def test_should_be_able_to_activate_chef_when_is_activated():
    chef = Chef(name='Test Chef', is_active=True)
    chef.activate()

    assert chef.is_active is True


def test_should_be_able_to_deactivate_chef_when_is_activated():
    chef = Chef(name='Test Chef', is_active=True)
    chef.deactivate()

    assert chef.is_active is False


def test_should_be_able_to_deactivate_chef_when_is_deactivated():
    chef = Chef(name='Test Chef', is_active=False)
    chef.deactivate()

    assert chef.is_active is False


def test_should_be_able_to_create_chef_when_provided_id():
    chef_id = uuid4()
    chef = Chef(id=chef_id, name='Test Chef', is_active=False)

    assert chef.id == chef_id


def test_should_be_able_to_create_chef_activated_when_not_provided_is_active():
    chef = Chef(name='Test Chef')

    assert chef.is_active is True
