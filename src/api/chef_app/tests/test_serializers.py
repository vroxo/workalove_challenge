from src.api.chef_app.serializers import CreateChefRequestSerializer


def test_when_create_chef_request_serializer_fields_are_valid():
    serializer = CreateChefRequestSerializer(
        data={
            'name': 'Chef',
        }
    )

    assert serializer.is_valid() is True


def test_when_is_active_is_not_provided_and_partial_then_do_not_add_it_to_serializer():
    serializer = CreateChefRequestSerializer(
        data={
            'name': 'Chef',
        },
        partial=True,
    )

    assert serializer.is_valid() is True
    assert 'is_active' not in serializer.validated_data


def test_when_is_active_is_not_provided_and_not_partial_then_set_to_true():
    serializer = CreateChefRequestSerializer(
        data={
            'name': 'Chef',
        },
    )
    assert serializer.is_valid() is True

    assert serializer.validated_data['is_active'] is True
