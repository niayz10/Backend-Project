from django.contrib import admin

# Register your models here.
from core.models import Comment, Book, Comics, CommentForComics

admin.site.register(Comment)
admin.site.register(Book)
admin.site.register(Comics)
admin.site.register(CommentForComics)