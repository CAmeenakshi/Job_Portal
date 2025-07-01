from accounts.models import EmployerProfile
from rest_framework import viewsets, permissions, filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.serializers import ValidationError  # 🔧 MODIFIED
from django_filters.rest_framework import DjangoFilterBackend
from .models import Job, Application, SavedJob, Company, CompanyReview
from .serializers import JobSerializer, ApplicationSerializer, SavedJobSerializer, CompanySerializer, CompanyReviewSerializer


class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['job_type', 'location']
    search_fields = ['title', 'description', 'requirements']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role == 'employer':
            return Job.objects.filter(employer=user)
        return Job.objects.all()

    def perform_create(self, serializer):
        if self.request.user.role != 'employer':
            raise PermissionDenied("Only employers can create job posts.")
        serializer.save(employer=self.request.user)

    def perform_update(self, serializer):
        job = self.get_object()
        if self.request.user != job.employer:
            raise PermissionDenied("Only the employer who created this job can update it.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.employer:
            raise PermissionDenied("Only the employer who created this job can delete it.")
        instance.delete()


class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'employer':
            return Application.objects.filter(job__employer=user)
        elif user.role == 'jobseeker':
            return Application.objects.filter(user=user)
        return Application.objects.none()

    def perform_create(self, serializer):
        job = serializer.validated_data['job']
        user = self.request.user
        if Application.objects.filter(job=job, user=user).exists():
            raise ValidationError("You have already applied for this job.")  # 🔧 MODIFIED
        serializer.save(user=user)

    def update(self, request, *args, **kwargs):
        application = self.get_object()
        if request.user.role == 'employer':
            if application.job.employer != request.user:
                raise PermissionDenied("You are not allowed to update this application.")
        elif request.user.role == 'jobseeker' and 'status' in request.data:
            raise PermissionDenied("Job seekers cannot update application status.")
        return super().update(request, *args, **kwargs)


class SavedJobViewSet(viewsets.ModelViewSet):
    serializer_class = SavedJobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavedJob.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        job = serializer.validated_data['job']
        if SavedJob.objects.filter(user=self.request.user, job=job).exists():
            raise ValidationError("You have already saved this job.")  # 🔧 MODIFIED
        serializer.save(user=self.request.user)


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.AllowAny]  # All can view 
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    
    search_fields = ['name', 'location']  # 🔍 Search support

    def perform_create(self, serializer):
        employer_profile = EmployerProfile.objects.get(user=self.request.user)
        serializer.save(employer=employer_profile)

    def perform_update(self, serializer):
        company = self.get_object()
        if company.employer.user != self.request.user:
            raise PermissionDenied("You can only update your own company.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.employer.user != self.request.user:
            raise PermissionDenied("You can only delete your own company.")
        instance.delete()

class CompanyReviewViewSet(viewsets.ModelViewSet):
    serializer_class = CompanyReviewSerializer
    permission_classes = [permissions.AllowAny]  # All can view
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['company']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'jobseeker':
            return CompanyReview.objects.all()
        elif user.role == 'employer':
            return CompanyReview.objects.filter(company__employer__user=user)
        return CompanyReview.objects.none()

    def perform_create(self, serializer):
        jobseeker_profile = self.request.user.jobseekerprofile
        company = serializer.validated_data['company']
        if CompanyReview.objects.filter(jobseeker=jobseeker_profile, company=company).exists():
            raise ValidationError("You already reviewed this company.")  # 🔧 MODIFIED
        serializer.save(jobseeker=jobseeker_profile)
