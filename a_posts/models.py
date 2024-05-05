from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class Post(models.Model):
    TYPE = [
        ('tanks', 'Танки'),
        ('healers', 'Хилы'),
        ('dd', 'ДД'),
        ('traders', 'Торговцы'),
        ('guildmasters', 'Гильдмастеры'),
        ('questgivers', 'Квестгиверы'),
        ('blacksmiths', 'Кузнецы'),
        ('letherworkers', 'Кожевники'),
        ('alchemists', 'Зельевары'),
        ('spellcasters', 'Мастера заклинаний')
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('Заголовок',max_length=64)
    category = models.CharField('Категория',max_length=20, choices=TYPE)
    created = models.DateTimeField('Дата создания',auto_now_add=True)
    content = RichTextUploadingField('Содержание',blank=True, null=True)
    likes = models.ManyToManyField(User, blank=True, related_name='likes', through='likedPost')

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created']


    def __str__(self):
        return f'{self.title}'
    
    def get_absolute_url(self):
        return reverse('post', args=[str(self.pk)])
    
class Response(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='responses')
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='responses')
    content = models.TextField('Содержание')
    created = models.DateTimeField('Дата создания',auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        try:
            return f'{self.author}: {self.content[:30]}...'
        except:
            return f'no author: {self.content[:30]}...'

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'
        ordering = ['-created'] 

class likedPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
        ordering = ['-created']

    def __str__(self):
        return f'{self.user.username} liked {self.post}'        