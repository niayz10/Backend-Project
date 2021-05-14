from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from core.models import Book, Comics


@receiver(post_delete, sender=Book)
def delete_rating_on_book(sender, instance, **kwargs):
    instance.file.delete()

@receiver(post_delete, sender=Comics)
def delete_rating_on_book(sender, instance, **kwargs):
    instance.file.delete()