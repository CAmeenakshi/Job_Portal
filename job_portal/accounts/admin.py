from django.contrib import admin
from .models import User
from .models import JobSeekerProfile, EmployerProfile


# Register your models here.
admin.site.register(User)

admin.site.register(JobSeekerProfile)
admin.site.register(EmployerProfile)