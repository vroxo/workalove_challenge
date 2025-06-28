from uuid import uuid4

from django.db import models


class ChefModel(models.Model):
    app_label = 'chef_app'

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'chefs'

    def __str__(self):
        return self.name
