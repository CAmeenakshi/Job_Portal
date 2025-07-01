
from django.db import models
from accounts.models import User , EmployerProfile, JobSeekerProfile # Assuming custom user model with employer role
from django.conf import settings
from django.db.models import Avg

# Create models for Job .
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

# Create models for Application .
class Application(models.Model):
    STATUS_CHOICES = [
    ('applied', 'Applied'),
    ('under_review', 'Under Review'),
    ('shortlisted', 'Shortlisted'),
    ('rejected', 'Rejected'),
    ('hired', 'Hired'),
]

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skills = models.TextField(blank=True)  # Optional field to enter skills
    cover_letter = models.TextField(blank=True)  # Optional cover letter
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)  # File upload
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')

    class Meta:
        unique_together = ['job', 'user']  # Prevent multiple applications


# Create models for SavedJob .
class SavedJob(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')  # Prevent saving the same job twice

    def __str__(self):
        return f"{self.user.email} saved {self.job.title}"
    
# Create models for Company. .  
class Company(models.Model):
    employer = models.OneToOneField(EmployerProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)
    
    def average_rating(self):
        return self.reviews.aggregate(avg=Avg('rating'))['avg'] or 0

class CompanyReview(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='reviews')
    jobseeker = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1)  # 1 to 5 stars
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['company', 'jobseeker']  # prevent multiple reviews




