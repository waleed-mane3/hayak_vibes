from import_export import resources
from .models import Card

class CardResource(resources.ModelResource):
    class Meta:
        model = Card