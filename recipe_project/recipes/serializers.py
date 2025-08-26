from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Ingredient, Recipe, RecipeIngredient


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']


class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'ingredient', 'quantity']


class RecipeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        allow_null=True,
        required=False
    )
    recipe_ingredients = RecipeIngredientSerializer(
        many=True,
        source='recipeingredient_set',
        read_only=True
    )
    # for creation
    ingredients_data = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        help_text="List of {'name': 'flour', 'quantity': '2 cups'} dicts"
    )

    class Meta:
        model = Recipe
        fields = '__all__'

    def _attach_ingredients(self, recipe, ingredients_data):
        for ing in ingredients_data:
            name = ing.get('name', '').strip().lower()
            qty = ing.get('quantity', '').strip()
            if not name:
                continue
            ingredient, _ = Ingredient.objects.get_or_create(name=name)
            RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient, quantity=qty)

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients_data', [])
        recipe = super().create(validated_data)
        self._attach_ingredients(recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients_data', [])
        instance = super().update(instance, validated_data)
        instance.recipeingredient_set.all().delete()
        self._attach_ingredients(instance, ingredients_data)
        return instance


class UserSerializer(serializers.ModelSerializer):
    recipes = RecipeSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'recipes']
        read_only_fields = ['id', 'recipes']
