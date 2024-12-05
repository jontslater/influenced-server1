from django.db import models

class Social(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, related_name='social')
    id = models.AutoField(primary_key=True)
    facebook = models.URLField(max_length=255, blank=True, null=True)
    instagram = models.URLField(max_length=255, blank=True, null=True)
    bluesky = models.URLField(max_length=255, blank=True, null=True)
    tiktok = models.URLField(max_length=255, blank=True, null=True)
    twitter = models.URLField(max_length=255, blank=True, null=True)
