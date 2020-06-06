from django.urls import path
from recipe import views

urlpatterns = [
    path('', views.index, name='homepage'),
    path('add_recipe/', views.add_recipe),
    path('author_add/', views.author_add),
    path('recipe_details/<int:id>/', views.recipe_details, name='recipes'),
    path('author/<int:id>/', views.author),
    path('login/', views.login_view),
    path('logout/', views.logout_view),

    path('recipe_edit/<int:id>/', views.recipe_edit, name="edit"),
    path('favorite/<int:id>/', views.favorite, name='favorite'),
    path('unfavorite/<int:id>/', views.unfavorite, name='unfavorite'),
]
