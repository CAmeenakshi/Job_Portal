
from django.db import models
from accounts.models import User  # Assuming custom user model with employer role
# Create your models here.

class Job(models.Model):
    JOB_TYPE_CHOICES = (
        ('full-time', 'Full Time'),
        ('part-time', 'Part Time'),
        ('internship', 'Internship'),
        ('remote', 'Remote'),
    )

    employer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'employer'})
    title = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField(null=True, blank=True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    location = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skills = models.TextField(blank=True)  # Optional field to enter skills
    cover_letter = models.TextField(blank=True)  # Optional cover letter
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)  # File upload
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['job', 'user']  # Prevent multiple applications
from django.db import models
from django.conf import settings
from .models import Job  # Adjust the import if Job is in another app

class SavedJob(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')  # Prevent saving the same job twice

    def __str__(self):
        return f"{self.user.email} saved {self.job.title}"


