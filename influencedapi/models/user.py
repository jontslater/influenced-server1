from django.db import models

class User(models.Model):
  bio = models.CharField(max_length=55)
  userName = models.CharField(max_length=55)
  rating = models.IntegerField()
  client = models.BooleanField(default=False)
  uid = models.CharField(max_length=50)
