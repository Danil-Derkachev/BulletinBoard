from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, verbose_name='Название категории')

    def __str__(self):
        return self.name


class Announcement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to='images/%Y/%m/%d',
        verbose_name='Изображения',
        validators=[FileExtensionValidator(allowed_extensions=['png'])]
    )
    file = models.FileField(
        null=True,
        blank=True,
        upload_to='files/%Y/%m/%d',
        verbose_name='Файлы',
        validators=[FileExtensionValidator(allowed_extensions=['docx'])]
    )
    video = models.FileField(
        null=True,
        blank=True,
        upload_to='videos/%Y/%m/%d',
        verbose_name='Видео',
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])]
    )

    def __str__(self):
        return f'{self.pk} : {self.title}'

    def get_absolute_url(self):
        return reverse('detail_announcement', kwargs={'pk': self.pk})


class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    text = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_accepted = models.BooleanField(default=False)

    def accept(self):
        self.is_accepted = True
        self.save()
