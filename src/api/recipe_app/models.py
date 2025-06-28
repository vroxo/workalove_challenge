from uuid import uuid4

from django.contrib.postgres.fields import ArrayField
from django.db import models

from src.api.chef_app.models import ChefModel


class RecipeModel(models.Model):
    app_label = 'recipe_app'

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True, default=None)
    is_active = models.BooleanField(default=True)
    ingredients = ArrayField(models.CharField(max_length=100), blank=False, default=list)
    preparation_method = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    chef = models.ForeignKey(
        ChefModel,
        on_delete=models.CASCADE,
        related_name='recipes',
        db_column='chef_id',
    )

    class Meta:
        db_table = 'recipes'

    def __str__(self):
        return self.name
