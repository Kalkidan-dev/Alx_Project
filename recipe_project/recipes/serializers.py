from models import Category, Ingredient, Recipe
from rest_framework import serializers
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'

class RecipeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True ,allow_null=True, required=False)
    ingredients = IngredientSerializer(many=True, read_only=True)
    ingredients_name = serializers.ListField(child=serializers.CharField(), write_only=True, help_text="List of ingredient names")

    class Meta:
        model = Recipe
        fields = '__all__'
    
    def _attach_ingredients(self, recipe, names):
        objs = []
        for n in names:
            n = n.strip().lower()
            if not n:
                continue
            ing, _ = Ingredient.objects.get_or_create(name=n)
            objs.append(ing)
        recipe.ingredients.add(*objs)

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients_name', [])
        recipe = super().create(validated_data)
        self._attach_ingredients(recipe, ingredients_data)
        return recipe
    
    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients_name', [])
        instance = super().update(instance, validated_data)
        instance.ingredients.clear()
        self._attach_ingredients(instance, ingredients_data)
        return instance

class UserSerializer(serializers.ModelSerializer):
    recipes = RecipeSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'recipes']
        read_only_fields = ['id', 'recipes']