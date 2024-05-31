# samj/models.py

from django.db import models
from django.contrib.auth.models import User

class Kopfnummer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=16)

    def __str__(self):
        return self.number

class Zielnummer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=16)
    number = models.CharField(max_length=16)

    def __str__(self):
        return self.number
