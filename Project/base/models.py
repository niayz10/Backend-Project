from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.
from auth_.models import CustomUser



class PublisherManager(models.Manager):

    def select_by_name(self):
        publishers = self.all().order_by('name')[:10]
        return publishers


class Publisher(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Название')
    address = models.TextField(null=True, blank=True, verbose_name='Адрес')
    website = models.CharField(max_length=100, null=True, blank=True, verbose_name='Веб сайт')
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name='Город')
    country = models.CharField(max_length=100, null=True, blank=True, verbose_name='Страна')

    objects = PublisherManager()

    class Meta:
        verbose_name = 'Издатель'
        verbose_name_plural = 'Издатели'

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Фамилия')
    email = models.CharField(max_length=255, null=True, blank=True, verbose_name='Почта')

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Mark(models.Model):
    mark = models.IntegerField(default=0, validators=[MaxValueValidator(10), MinValueValidator(0)])
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Rating(models.Model):
    _marks = models.ManyToManyField(Mark)

    @property
    def count(self):
        return len(self._marks.all())

    @property
    def average(self):
        if self.count == 0:
            return 0
        sum = 0
        for mark in self._marks.all():
            sum += mark.mark
        return sum / self.count

    def add_mark(self, user, mark):
        for mark in self._marks.all():
            if mark.user == user:
                return
        mark = Mark.objects.create(mark=mark, user=user)
        self._marks.add(mark)
        return mark


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Категория")
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'Categories'


class Genre(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'Genres'


class Type(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'Types'


class JournalBase(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name='Название')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    publication_date = models.DateField(verbose_name='Дата создания', auto_now_add=True)
    genre = models.ManyToManyField(Genre)
    rating = models.OneToOneField(Rating, on_delete=models.CASCADE, verbose_name='Рейтинг')
    author = models.ForeignKey(Author, on_delete=models.RESTRICT, verbose_name='Автор')
    publisher = models.ForeignKey(Publisher, on_delete=models.RESTRICT, verbose_name='Издатель')

    class Meta:
        abstract = True
