from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib import messages



@receiver(post_save,sender=User)
def create_profile(sender,instance,created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_profile(sender,instance, **kwargs):
    instance.profile.save()

@receiver(user_logged_in)
def log_user_in(sender, user, request, **kwargs):
    messages.success(request, f'Welcome back, {user.username}! Login successful.')

@receiver(user_logged_out)
def log_user_out(sender, user, request, **kwargs):
    if user is not None:
        messages.info(request, 'You have been successfully logged out.')
    else:
        messages.info(request, 'You have been successfully logged out.')
