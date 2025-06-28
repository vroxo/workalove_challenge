from rest_framework import serializers


class StringListField(serializers.ListField):
    def to_internal_value(self, data):
        for item in data:
            if not isinstance(item, str):
                raise serializers.ValidationError('All elements must be strings.')

        data = super().to_internal_value(data)
        return data


class CreateRecipeRequestSerializer(serializers.Serializer):
    chef_id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(
        max_length=255, required=False, allow_blank=True, allow_null=True
    )
    ingredients = StringListField(
        child=serializers.CharField(),
        allow_empty=False,
        min_length=1,
    )
    preparation_method = serializers.CharField(max_length=500)
    is_active = serializers.BooleanField(default=True)


class CreateRecipeResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class RecipeErrorResponseSerializer(serializers.Serializer):
    detail = serializers.CharField(max_length=255)


class UpdateRecipeRequestSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=255)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=False)
    ingredients = StringListField(
        child=serializers.CharField(),
        allow_empty=False,
        min_length=1,
        required=False,
    )
    preparation_method = serializers.CharField(required=False, max_length=500)
    is_active = serializers.BooleanField(required=False)


class DeleteRecipeRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class RecipeResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    chef_id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(allow_blank=True, allow_null=False)
    ingredients = StringListField(
        child=serializers.CharField(),
        allow_empty=False,
        min_length=1,
    )
    preparation_method = serializers.CharField(max_length=500)
    is_active = serializers.BooleanField()


class ListRecipeResponseSerializer(serializers.Serializer):
    data = RecipeResponseSerializer(many=True)
