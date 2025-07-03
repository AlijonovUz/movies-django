from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView

from .models import Genres, Movies
from .forms import GenreForms, MovieForms, LoginForms


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


class GenreCreateView(PermissionRequiredMixin, CreateView):
    model = Genres
    form_class = GenreForms
    success_url = reverse_lazy('home')
    permission_required = 'manager.add_genres'

    def handle_no_permission(self):
        return redirect('home')

    def form_valid(self, form):
        genre = form.instance
        messages.success(self.request, f"{genre.name} janri muvaffaqiyatli qo'shildi.")
        return super().form_valid(form)


class GenreUpdateView(PermissionRequiredMixin, UpdateView):
    model = Genres
    form_class = GenreForms
    success_url = reverse_lazy('home')
    slug_url_kwarg = 'slug'
    permission_required = 'manager.change_genres'

    def handle_no_permission(self):
        return redirect('home')

    def form_valid(self, form):
        genre = self.get_object()
        messages.success(self.request, f"{genre.name} janri muvaffaqiyatli yangilandi.")
        return super().form_valid(form)


class GenreDeleteView(PermissionRequiredMixin, View):
    permission_required = 'manager.delete_genres'

    def handle_no_permission(self):
        return redirect('home')

    def post(self, request, slug):
        genre = get_object_or_404(Genres, slug=slug)
        genre.delete()
        messages.success(request, f"{genre.name} janri muvaffaqiyatli o'chirildi.")
        return redirect('home')


class MovieCreateView(PermissionRequiredMixin, CreateView):
    model = Movies
    form_class = MovieForms
    success_url = reverse_lazy('home')
    permission_required = 'manager.add_movies'

    def handle_no_permission(self):
        return redirect('home')

    def form_valid(self, form):
        movie = form.instance
        messages.success(self.request, f"{movie.name} filmi muvaffaqiyatli qo'shildi.")
        return super().form_valid(form)


class MovieUpdateView(PermissionRequiredMixin, UpdateView):
    model = Movies
    form_class = MovieForms
    success_url = reverse_lazy('home')
    slug_url_kwarg = 'slug'
    permission_required = 'manager.change_movies'

    def handle_no_permission(self):
        return redirect('home')

    def form_valid(self, form):
        movie = self.get_object()
        messages.success(self.request, f"{movie.name} filmi muvaffaqiyatli yangilandi.")
        return super().form_valid(form)


class MovieDeleteView(PermissionRequiredMixin, View):
    permission_required = 'manager.delete_movies'

    def handle_no_permission(self):
        return redirect('home')

    def post(self, request, slug):
        movie = get_object_or_404(Movies, slug=slug)
        movie.delete()
        messages.success(request, f"{movie.name} filmi muvaffaqiyatli o'chirildi.")
        return redirect('home')


class Login(LoginView):
    form_class = LoginForms
    template_name = 'registrations/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, "Siz muvaffaqiyatli tizimga kirdingiz!")
        return super().form_valid(form)


class Logout(LoginRequiredMixin, View):

    login_url = reverse_lazy('home')

    def get(self, request):
        logout(request)
        messages.success(self.request, "Siz muvaffaqiyatli tizimdan chiqdingiz!")
        return redirect('login')


class Custom404View(TemplateView):
    template_name = '404.html'
