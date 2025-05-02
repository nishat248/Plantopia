from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, AdminProfile
from django.contrib.auth import get_user_model

User = get_user_model()

# --- For normal user Profile ---
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not instance.is_staff and not instance.is_superuser:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()

# --- For AdminProfile ---
@receiver(post_save, sender=User)
def create_admin_profile(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        AdminProfile.objects.create(user=instance)
    else:
        if instance.is_superuser and not hasattr(instance, 'adminprofile'):
            AdminProfile.objects.create(user=instance)
