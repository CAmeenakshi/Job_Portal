from django.contrib import admin
from .models import Job,Application,SavedJob,Company,CompanyReview
# Register your models here.
admin.site.register(Job)
admin.site.register(Application)
admin.site.register(SavedJob)
admin.site.register(Company)
admin.site.register(CompanyReview)
