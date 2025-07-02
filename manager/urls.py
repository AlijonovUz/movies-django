from django.urls import path

from .views import *

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('search/', SearchView.as_view(), name='search'),

    path('genre/<slug:slug>', MoviesByGenre.as_view(), name='genre'),
    path('movie/<slug:slug>.html', MovieDetail.as_view(), name='movie')
]