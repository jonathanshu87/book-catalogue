from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

app_name= 'books'

urlpatterns = [
    path('home/', views.HomePage.as_view(), name='home'),
    path('', LoginView.as_view(template_name='login.html'), name="login"),
    path('delete/<pk>', views.book_delete, name='book_delete'),
]