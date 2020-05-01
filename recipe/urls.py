from django.urls import path
from recipe import views

urlpatterns = [
    path('', views.index),
    path('recipe_details/<int:id>/', views.recipe_details),
    path('author/<int:id>/', views.author)
]
