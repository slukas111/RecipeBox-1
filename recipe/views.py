from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from recipe.models import Recipe, Author
from recipe.forms import AddRecipeForm, AddAuthorForm, LoginForm, RecipeEditForm



def login_view(request):
    html = "generic_form.html"

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data["username"], password=data["password"]
            )
            if user:
                login(request, user)
                return HttpResponseRedirect(
                    request.GET.get("next", reverse("homepage"))
                )
    form = LoginForm()
    return render(request, html, {"form": form})


def logout_view(request):
    if request.user:
        logout(request)
    return HttpResponseRedirect(reverse("homepage"))


def index(request):
    data = Recipe.objects.all()
    author = Author.objects.all()
    return render(request, "index.html", {"data": data, "author": author})


@login_required
def add_recipe(request):
    html = "generic_form.html"

    if request.method == "POST":
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data["title"],
                author=data["author"],
                description=data["description"],
                time_required=data["time_required"],
                instructions=data["instructions"],
            )
        return HttpResponseRedirect(reverse("homepage"))
    form = AddRecipeForm()
    return render(request, html, {'form': form})


@login_required
@staff_member_required
def author_add(request):
    html = "author_add.html"
    form = AddAuthorForm()
    if request.method == "POST":
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            author = User.objects.create_user(username=data["name"])
            Author.objects.create(user=author, name=data["name"], bio=data.get("bio"))
        return HttpResponseRedirect(reverse("homepage"))

    return render(request, html, {"form": form})


def recipe_details(request, id):
    data = Recipe.objects.get(id=id)
    if data in request.user.author.favorites.all(): 
        favorites = True 
    else:
        favorites = False
    return render(request, "recipe_details.html", {"data": data, "favorites": favorites})


def author(request, id):
    data = Author.objects.get(id=id)
    user_data = Recipe.objects.filter(author=Author.objects.get(id=id))
    favorites = data.favorites.all()
    return render(request, "author.html", {"data": data, "user_data": user_data, "favorites": favorites})



@login_required
def favorite(request, id):
    username = request.user.author
    favrecipe = Recipe.objects.get(id=id)
    username.favorites.add(favrecipe)

    return HttpResponseRedirect(reverse('recipes', kwargs={'id':id}))

@login_required
def unfavorite(request, id):
    username = request.user.author
    favrecipe = Recipe.objects.get(id=id)
    username.favorites.remove(favrecipe)

    return HttpResponseRedirect(reverse('recipes', kwargs={'id':id}))


def recipe_edit(request, id):
    html = "recipe_edit.html"
    recipe = Recipe.objects.get(id=id)
    if request.method == "POST":
        form = RecipeEditForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            recipe.title = data["title"]
            recipe.description = data["body"]
            recipe.save()
            return HttpResponseRedirect(reverse("recipes", args=(id,)))
    form = RecipeEditForm(initial={"title": recipe.title, "body": recipe.description})
    return render(request, html, {"form": form, "recipe": recipe})

