from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # fields = ['name']
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        return representation