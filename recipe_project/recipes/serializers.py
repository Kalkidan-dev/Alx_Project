from .models import Category, Ingredient, Recipe, RecipeIngredient
from rest_framework import serializers
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'quantity']


class RecipeIngredientSerializer(serializers.ModelSerializer):
    # Represent the Ingredient inline (name + quantity)
    name = serializers.CharField(source="ingredient.name")
    quantity = serializers.CharField()

    class Meta:
        model = RecipeIngredient
        fields = ['name', 'quantity']


class RecipeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category'
    )

    # For input
    ingredients = serializers.ListSerializer(
        child=serializers.DictField(), write_only=True
    )

    # For output
    ingredients_details = RecipeIngredientSerializer(
        many=True, read_only=True, source='recipeingredient_set'
    )

    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'instructions',
            'category_id', 'owner',
            'ingredients', 'ingredients_details',
            'preparation_time', 'cooking_time', 'servings',
            'created_at', 'updated_at'
        ]

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients', [])
        validated_data.pop('owner', None)

        recipe = Recipe.objects.create(owner=self.context['request'].user, **validated_data)

        for ing in ingredients_data:
            name = ing.get('name', '').strip().lower()
            quantity = ing.get('quantity', '')
            if not name or not quantity:
                raise serializers.ValidationError("Each ingredient must include a name and quantity.")

            ingredient_obj, _ = Ingredient.objects.get_or_create(name=name)
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient_obj,
                quantity=quantity
            )

        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients', [])
        validated_data.pop('owner', None)

        instance = super().update(instance, validated_data)

        # Clear old ingredients
        instance.recipeingredient_set.all().delete()

        for ing in ingredients_data:
            name = ing.get('name', '').strip().lower()
            quantity = ing.get('quantity', '')
            if not name or not quantity:
                raise serializers.ValidationError("Each ingredient must include a name and quantity.")

            ingredient_obj, _ = Ingredient.objects.get_or_create(name=name)
            RecipeIngredient.objects.create(
                recipe=instance,
                ingredient=ingredient_obj,
                quantity=quantity
            )

        return instance


class UserSerializer(serializers.ModelSerializer):
    recipes = RecipeSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'recipes']
        read_only_fields = ['id', 'recipes']
