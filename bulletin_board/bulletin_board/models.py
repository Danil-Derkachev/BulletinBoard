from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from .resources import CATEGORIES


class Announcement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to='images', verbose_name='Изображения')
    category = models.CharField(max_length=2, choices=CATEGORIES)

    def __str__(self):
        return f'{self.pk} : {self.title}'

    def get_absolute_url(self):
        return reverse('detail_announcement', kwargs={'pk': self.id})


class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    text = models.TextField()
