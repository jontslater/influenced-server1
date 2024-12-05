from django.db import models

class User(models.Model):
    bio = models.CharField(max_length=255, blank=True, null=True)
    userName = models.CharField(max_length=55, null=True, blank=True, unique=True)
    rating = models.IntegerField(default=0)
    client = models.BooleanField(default=False)
    uid = models.CharField(max_length=50, unique=True)
    socials = models.ForeignKey("Social", on_delete=models.CASCADE)
