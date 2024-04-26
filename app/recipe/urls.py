"""
Recipe API URL management
"""

from recipe.views import (
    RecipeViewSet,
    TagViewSet
)
from django.urls import (
    path,
    include
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('recipes', RecipeViewSet)
router.register('tags', TagViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]
