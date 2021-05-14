from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from auth_.models import CustomUser, Profile
from utils.upload import user_avatar_delete


@receiver(post_save, sender=CustomUser)
def user_created(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_delete, sender=CustomUser)
def delete_file_on_custom_user_delete(sender, instance, **kwargs):
    avatar = instance.avatar
    if avatar:
        user_avatar_delete(avatar)
