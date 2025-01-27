from django.db import models

class Job(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField()
    created_on = models.DateField(auto_now_add=True)
    client_id = models.ForeignKey('User', on_delete=models.CASCADE, related_name='jobs')
    accepted = models.BooleanField(default=False)
    pay = models.CharField(max_length=100)
    acceptedBy = models.ForeignKey('User', on_delete=models.CASCADE, related_name='accepted_jobs', null=True, blank=True)
    complete = models.BooleanField(default=False)
    
    # Add the hasApplied field to track job applications
    hasApplied = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.description[:50]} - {self.pay}"
