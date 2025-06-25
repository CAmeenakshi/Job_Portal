from django.db import models
import enum
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

# Create your models here.
class RoleEnum(enum.Enum):
    JOBSEEKER = "jobseeker"
    EMPLOYER = "employer"

class User(AbstractUser):
    ROLE_CHOICES = (
        (RoleEnum.JOBSEEKER.value,'jobseeker'),
        (RoleEnum.EMPLOYER.value,'employer'),
    )

    username = None
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100,null = True)
    phone_number = models.CharField(max_length= 15,blank = True,null = True)
    role = models.CharField(max_length=10,choices = ROLE_CHOICES,null=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    
    objects = CustomUserManager()
            

    def __str__(self):
        return self.full_name

class JobSeekerProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/',null=True)
    skills = models.TextField(blank=True, null=True)
    experience = models.PositiveIntegerField(default=0)
    education = models.TextField(blank = True,null = True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email
    
class EmployerProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255,null=True)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    company_website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True,null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name
