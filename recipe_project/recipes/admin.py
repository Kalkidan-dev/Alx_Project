from django.contrib import admin
from .models import Recipe, Category, Ingredient, RecipeIngredient

# ----------------- Recipe Management -----------------
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'category', 'created_at')
    search_fields = ('title', 'owner__username', 'category__name')
    list_filter = ('category',)
    ordering = ('-created_at',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'quantity')
    search_fields = ('recipe__title', 'ingredient__name')
    ordering = ('recipe',)
