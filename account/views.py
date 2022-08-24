from django.shortcuts import render, redirect
from account.forms import BookForm
from account.models import Book
from django.views.generic import TemplateView
import account.recommendation as recommendation
import random 
import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

class HomePage(TemplateView):
    template_name = 'home.html'

    def get(self, request):
        if 'generate' in request.GET:
            books = Book.objects.all()
            recBooks = dict()
            if books.count() >= 5 :
                sample = random.sample(range (0, books.count()), 5)
                for i in sample:
                    if (books[i].rating >= 3):
                        recBooks[(books[i].title, books[i].author)] = recommendation.run(books[i].title, books[i].author)
            form = BookForm()
            books = Book.objects.all()
            context = {'form': form, 'books':books, 'recBooks' : recBooks}
            return render(request, self.template_name, context)
        else: 
            form = BookForm()
            books = Book.objects.all()
            args = {'form': form, 'books':books}
            return render(request, self.template_name, args)

    def post(self,request):
        if 'save' in request.POST:
            form = BookForm(request.POST)
            if form.is_valid():
                form.save()
                title = form.cleaned_data['title']
                author = form.cleaned_data['author']
                rating = form.cleaned_data['rating']


            books = Book.objects.all()
            args = {'form': form, 'title': title, 'author': author, 'rating': rating, 'books': books}
            return render(request, self.template_name, args)
    

def book_delete(request, pk):
    book = get_object_or_404(Book, title=pk)  
    if request.method == 'POST':         
        book.delete()                     
        return redirect('/home/')             

    return render(request, 'home.html', {'book': book})
        
            



