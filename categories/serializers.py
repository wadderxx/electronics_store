from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Category name cannot be empty."
            )
        return value