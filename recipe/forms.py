from django import forms
from recipe.models import Author


class AddAuthorForm(forms.ModelForm):
    class Meta():
        model = Author
        fields = ['name', 'bio']


class AddRecipeForm(forms.Form):
    title = forms.CharField(max_length=50)
    author = forms.ModelChoiceField(queryset=Author.objects.all())
    description = forms.CharField(widget=forms.Textarea)
    time_required = forms.CharField(max_length=50)
    instructions = forms.CharField(widget=forms.Textarea)
