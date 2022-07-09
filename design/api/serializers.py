from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from design.models import Design


# This is used to update #first_sign_in# field
class AllDesignsSerializer(ModelSerializer):
    class Meta:

        model = Design
        fields = ['id', 'name', 'image']