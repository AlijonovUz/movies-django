from django.contrib import admin

from .models import *


@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    list_per_page = 10

    actions_on_top = False
    actions_on_bottom = True

    prepopulated_fields = {
        'slug': ('name',)
    }


@admin.register(Movies)
class MoviesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    list_per_page = 10

    actions_on_top = False
    actions_on_bottom = True

    prepopulated_fields = {
        'slug': ('name',)
    }

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'genre':
            queryset = Genres.objects.all()
            kwargs['queryset'] = queryset

            if not queryset.exists() and not hasattr(request, '_genre_warning_shown'):
                self.message_user(request, "Hech qanday janr mavjud emas!", level='warning')
                request._genre_warning_shown = True

        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name in ['language', 'age']:
            kwargs['choices'] = [('', 'Tanlang')] + list(db_field.choices)
            
        return super().formfield_for_choice_field(db_field, request, **kwargs)