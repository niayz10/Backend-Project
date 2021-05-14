from django.db import models

# Create your models here.
from auth_.models import CustomUser
from base.models import JournalBase, Category, Type, Rating
from utils.validators import validate_extension_for_book, validate_extension_for_comics


class BookManager(models.Manager):

    def create(self, **extra_fields):
        rating = Rating.objects.create()
        content = self.model(**extra_fields)
        content.rating = rating
        content.save(using=self._db)
        return content


class Book(JournalBase):
    num_pages = models.IntegerField(default=0, verbose_name='Количество страниц')
    file = models.FileField(upload_to="book storage", validators=[validate_extension_for_book], null=True, blank=True)
    objects = BookManager()


class ComicsManager(models.Manager):

    def create(self, **extra_fields):
        rating = Rating.objects.create()
        content = self.model(**extra_fields)
        content.rating = rating
        content.save(using=self._db)
        return content


class Comics(JournalBase):
    type = models.ManyToManyField(Type, related_name="comics", verbose_name="Тип")
    category = models.ManyToManyField(Category, related_name="comics", verbose_name="Категория")
    num_of_chapters = models.IntegerField(default=0)
    file = models.FileField(upload_to="comics storage", validators=[validate_extension_for_comics], null=True, blank=True)


    objects = ComicsManager()


class Comment(models.Model):
    date = models.DateField(verbose_name='Дата создания', auto_now_add=True)
    content = models.TextField(verbose_name='Текст')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    journal = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="comments")


class CommentForComics(models.Model):
    date = models.DateField(verbose_name='Дата создания', auto_now_add=True)
    content = models.TextField(verbose_name='Текст')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    journal = models.ForeignKey(Comics, on_delete=models.CASCADE, related_name="comments")
