from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView

from .models import Genres, Movies


class HomeListView(ListView):
    model = Genres
    context_object_name = 'genres'
    template_name = 'index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()

        movies = Movies.objects.all().prefetch_related('genre')
        paginator = Paginator(movies, 3)
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.page(page_number)

        context.update({
            'movies': page_obj.object_list,
            'page_obj': page_obj,
            'is_paginated': page_obj.has_other_pages()
        })

        return context


class MoviesByGenre(ListView):
    template_name = 'index.html'
    context_object_name = 'movies'
    paginate_by = 3

    def get_queryset(self):
        genre = get_object_or_404(Genres, slug=self.kwargs.get('slug'))
        return Movies.objects.filter(genre=genre).prefetch_related('genre')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()

        context.update({
            'genres': Genres.objects.all()
        })

        return context


class MovieDetail(DetailView):
    model = Movies
    template_name = 'detail.html'
    context_object_name = 'movie'
    slug_url_kwarg = 'slug'

    def get(self, request, *args, **kwargs):
        movie = self.get_object()
        if movie.age == '18+':
            messages.warning(request, "Diqqat! Ushbu film 18 yoshdan kattalar uchun tavsiya etiladi.")
        elif movie.age == '21+':
            messages.warning(request, "Diqqat! Ushbu film 21 yoshdan kattalar uchun tavsiya etiladi.")
        return super().get(request, *args, **kwargs)


class SearchView(ListView):
    template_name = 'index.html'
    context_object_name = 'movies'
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '').strip()
        if not query:
            redirect('home')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        return Movies.objects.filter(name__icontains=query)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()

        context.update({
            'genres': Genres.objects.all()
        })

        return context


class Custom404View(TemplateView):
    template_name = '404.html'
