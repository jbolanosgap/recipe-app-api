"""
Serializers for recipe API'
"""

from core.models import (
    Recipe,
    Tag,
    Ingredient,
)
from rest_framework import serializers


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredients."""

    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""
    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'time_minutes',
            'price',
            'link',
            'tags',
            'ingredients'
        ]
        read_only_fields = ['id']

    def _get_or_create_items(self, items, recipe, model_class, relation_name):
        """Handle getting or creating tags as needed."""
        auth_user = self.context['request'].user
        for item in items:
            item_obj, created = model_class.objects.get_or_create(
                user=auth_user,
                **item,
            )
            getattr(recipe, relation_name).add(item_obj)

    def create(self, validated_data):
        """Create a recipe."""
        tags = validated_data.pop('tags', [])
        ingredients = validated_data.pop('ingredients', [])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_items(tags, recipe, Tag, 'tags')
        self._get_or_create_items(
            ingredients,
            recipe,
            Ingredient,
            'ingredients'
        )

        return recipe

    def update(self, instance, validated_data):
        """Update recipe."""
        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredients', None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_items(tags, instance, Tag, 'tags')
        if ingredients is not None:
            instance.ingredients.clear()
            self._get_or_create_items(
                ingredients,
                instance,
                Ingredient,
                'ingredients'
            )

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail"""
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']
