from django.shortcuts import render

from recipe.models import Recipe, Author


# Create your views here.
def index(request):
    data = Recipe.objects.all()
    return render(request, 'index.html', {'data': data})


def recipe_details(request, id):
    data = Recipe.objects.get(id=id)
    return render(request, 'recipe_details.html', {'data': data})


def author(request, id):
    data = Author.objects.get(id=id)
    recipes = Recipe.objects.filter(author=Author.objects.get(id=id))
    return render(request, 'author.html', {'data': data, 'recipes': recipes})
