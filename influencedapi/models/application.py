from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Application(models.Model):
    id = models.AutoField(primary_key=True)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posted_applications")
    job = models.ForeignKey('Job', on_delete=models.CASCADE, related_name='applications')
    applied_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['applicant', 'job']

    def __str__(self):
        return f"Application by {self.applicant.userName} for job {self.job.id} by {self.poster.userName}"
