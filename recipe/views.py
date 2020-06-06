from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


from recipe.models import Recipe, Author
from recipe.forms import AddRecipeForm, AddAuthorForm, LoginForm


# Create your views here.
def login_view(request):
    html = "generic_form.html"

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request,
                username=data['username'],
                password=data['password']
                )
            if user:
                login(request, user)
                return HttpResponseRedirect(
                    request.GET.get('next', reverse('homepage'))
                    )
    form = LoginForm()
    return render(request, html, {'form': form})


def logout_view(request):
    if request.user:
        logout(request)
    return HttpResponseRedirect(reverse('homepage'))


def index(request):
    data = Recipe.objects.all()
    return render(request, 'index.html', {'data': data})


@login_required
def add_recipe(request):
    html = "generic_form.html"

    if request.method == "POST":
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data['title'],
                author=data['author'],
                description=data['description'],
                time_required=data['time_required'],
                instructions=data['instructions'],
                )
        return HttpResponseRedirect(reverse('homepage'))
    form = AddRecipeForm()
    return render(request, html, {'form': form})


@staff_member_required
def add_author(request):
    html = "generic_form.html"

    if request.method == "POST":
        form = AddAuthorForm(request.POST)
        form.save()
        return HttpResponseRedirect(reverse('homepage'))

    form = AddAuthorForm()
    return render(request, html, {'form': form})


def recipe_details(request, id):
    data = Recipe.objects.get(id=id)
    return render(request, 'recipe_details.html', {'data': data})


def author(request, id):
    data = Author.objects.get(id=id)
    recipes = Recipe.objects.filter(author=Author.objects.get(id=id))
    return render(request, 'author.html', {'data': data, 'recipes': recipes})
