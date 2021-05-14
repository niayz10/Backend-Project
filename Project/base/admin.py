from django.contrib import admin

# Register your models here.
from base.models import Publisher, Author, Rating, Mark

admin.site.register(Publisher)
admin.site.register(Author)
admin.site.register(Rating)
admin.site.register(Mark)