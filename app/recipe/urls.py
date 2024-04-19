"""
Recipe API URL management
"""

from recipe.views import RecipeViewSet
from django.urls import (
    path,
    include
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('recipes', RecipeViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]
