from django import forms
from account.models import Book

class BookForm(forms.ModelForm):
    title = forms.CharField()
    author = forms.CharField()
    rating = forms.IntegerField(min_value=0,max_value=5)

    class Meta:
        model = Book
        fields = ('title', 'author', 'rating')

