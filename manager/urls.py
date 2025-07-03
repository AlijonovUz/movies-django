from django.urls import path

from .views import *

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('search/', SearchView.as_view(), name='search'),

    path('auth/login/', Login.as_view(), name='login'),
    path('auth/logout/', Logout.as_view(), name='logout'),

    path('genre/<slug:slug>', MoviesByGenre.as_view(), name='genre'),
    path('movie/<slug:slug>.html', MovieDetail.as_view(), name='movie'),

    path('add-genre/', GenreCreateView.as_view(), name='add-genre'),
    path('update-genre/<slug:slug>', GenreUpdateView.as_view(), name='update-genre'),
    path('delete-genre/<slug:slug>', GenreDeleteView.as_view(), name='delete-genre'),

    path('add-movie/', MovieCreateView.as_view(), name='add-movie'),
    path('update-movie/<slug:slug>.html', MovieUpdateView.as_view(), name='update-movie'),
    path('delete-movie/<slug:slug>.html', MovieDeleteView.as_view(), name='delete-movie'),
]