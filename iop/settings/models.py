from django.db import models
#new code for userPFP
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar_url = models.URLField(blank=True)
    gender = models.CharField(blank = True, max_length=20)
    age = models.IntegerField(null=True, blank=False)

    def __str__(self):
        return f'Profil {self.user.username}'