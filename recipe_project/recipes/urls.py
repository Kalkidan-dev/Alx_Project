from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, IngredientViewSet, RecipeViewSet, UserViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'users', UserViewSet)

urlpatterns = router.urls
