from django.db import models

class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    job = models.ForeignKey('Job', on_delete=models.CASCADE, related_name='ratings')
    user_rating = models.IntegerField()
    client_rating = models.IntegerField()
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_ratings')
    client = models.ForeignKey('User', on_delete=models.CASCADE, related_name='client_ratings')

    def __str__(self):
        return f'Rating for Job {self.job.id} by User {self.user.id}'
