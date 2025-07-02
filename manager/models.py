from datetime import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .validators import validate_video_file_extension


class Genres(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Nomi')
    slug = models.SlugField(max_length=150, unique=True, verbose_name='Identifikator')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Janr '
        verbose_name_plural = 'Janrlar'


LANGUAGE_CHOICES = (
    ("O'zbek tilida", "O'zbek tilida"),
    ("Rus tilida", "Rus tilida"),
    ("Ingliz tilida", "Ingliz tilida")
)

AGE_LIMIT = (
    ('0+', "0+"),
    ('6+', "6+"),
    ('16+', "16+"),
    ('18+', "18+"),
    ('21+', "21+"),
)


class Movies(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nomi')
    slug = models.SlugField(max_length=150, unique=True, verbose_name='Identifikator')
    genre = models.ManyToManyField(Genres, related_name='genre', verbose_name='Janr')
    country = models.CharField(max_length=50, verbose_name='Davlati')
    year = models.IntegerField(default=1900, verbose_name='Yili',
                               validators=[MinValueValidator(1900), MaxValueValidator(datetime.now().year)])
    language = models.CharField(max_length=13, choices=LANGUAGE_CHOICES, verbose_name='Tili')
    duration = models.CharField(max_length=20, default='1 soat 40 daqiqa', verbose_name='Davomiyligi')
    age = models.CharField(max_length=3, choices=AGE_LIMIT, verbose_name='Yosh chegarasi')
    photo = models.ImageField(upload_to='photo/', verbose_name='Surati')
    video = models.FileField(upload_to='video/', validators=[validate_video_file_extension], verbose_name='Videosi')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kino '
        verbose_name_plural = 'Kinolar'
