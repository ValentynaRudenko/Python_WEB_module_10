from django.urls import path
from . import views

app_name = 'quoteapp'

urlpatterns = [
    path('', views.main, name='main'),
    path('quote/', views.quote, name='quote'),
    path('author/', views.author, name='author'),
    path('tag/', views.tag, name='tag'),
    path('quote_list/', views.quote_list, name='quote_list'),
    path('quote_detail/<int:quote_id>',
         views.quote_detail,
         name='quote_detail'),
    path('delete/<int:quote_id>', views.delete_quote, name='delete'),
    path('author_detail/<int:author_id>',
         views.author_detail,
         name='author_detail'),
    path('delete/<int:author_id>', views.delete_author, name='delete'),
]
