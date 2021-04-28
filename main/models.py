from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models as gis_models

from main.api import service


class Profile(models.Model):
    rate = (
        ('Base', 'base'),
        ('Premium', 'premium'),
        ('VIP', 'vip'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    image = models.ImageField(upload_to='image/', null=True)
    phone = models.CharField(max_length=30, null=True)
    name = models.CharField(max_length=100, null=True)
    surname = models.CharField(max_length=100, null=True)
    group = models.CharField(max_length=100, choices=rate, default='base', null=True)
    geo_location = gis_models.PointField(srid=4326, null=True, blank=True, default=service.get_location())

    def __str__(self):
        return self.user.username


class AddContent(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Профиль')
    image = models.ImageField(upload_to='image/profiles')
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def save_or_create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        try:
            instance.profile.save()
        except ObjectDoesNotExist:
            Profile.objects.create(user=instance)



