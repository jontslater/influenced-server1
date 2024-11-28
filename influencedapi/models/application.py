from django.db import models

class Application(models.Model):
    id = models.AutoField(primary_key=True)
    applicant = models.ForeignKey('User', on_delete=models.CASCADE)
    poster = models.ForeignKey('User', on_delete=models.CASCADE, related_name="posted_applications")
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    applied_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending',
    )
    message = models.TextField(null=True, blank=True)  # New field for the applicant's message

    def __str__(self):
        return f"Application by {self.applicant.userName} for job {self.job.id}"
