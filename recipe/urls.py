from django.urls import path
from recipe import views

urlpatterns = [
    path('', views.index, name='homepage'),
    path('add_recipe/', views.add_recipe),
    path('add_author/', views.add_author),
    path('recipe_details/<int:id>/', views.recipe_details),
    path('author/<int:id>/', views.author)
]
