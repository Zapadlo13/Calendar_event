from django.contrib.auth.models import User
from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=128, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', blank=True)
    start_time = models.DateTimeField(verbose_name='Начало события', blank=True)
    end_time = models.DateTimeField(verbose_name='Конец события', blank=True)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
