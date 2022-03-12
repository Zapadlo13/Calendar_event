from django.contrib.auth.models import User
from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=64, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', blank=True)
    date_event = models.DateField(verbose_name='Дата события')
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
