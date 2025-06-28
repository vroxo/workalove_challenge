from rest_framework import serializers


class CreateChefRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField(default=True)


class CreateChefResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class ChefErrorResponseSerializer(serializers.Serializer):
    detail = serializers.CharField(max_length=255)
