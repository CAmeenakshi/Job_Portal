
from rest_framework import viewsets, permissions,serializers
from rest_framework.exceptions import PermissionDenied
from .models import Job,Application,SavedJob
from .serializers import JobSerializer,ApplicationSerializer,SavedJobSerializer

class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role == 'employer':
            return Job.objects.filter(employer=user)
        return Job.objects.all()  # For seekers and public

    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

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
        # Employers should see applications for jobs they have posted
         return Application.objects.filter(job__employer=user)
        elif user.role == 'jobseeker':
        # Job seekers should only see applications they have submitted
         return Application.objects.filter(user=user)
        return Application.objects.none()  # For safety, if role doesn't match


    def perform_create(self, serializer):
        job = serializer.validated_data['job']
        user = self.request.user
        if Application.objects.filter(job=job, user=user).exists():
            raise serializers.ValidationError("You have already applied for this job.")
        serializer.save(user=user)
    def update(self, request, *args, **kwargs):
        application = self.get_object()

        if request.user.role == 'employer':
            if application.job.employer != request.user:
                raise PermissionDenied("You are not allowed to update this application.")
        elif request.user.role == 'jobseeker':
            # prevent seekers from changing status
            if 'status' in request.data:
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
            raise serializers.ValidationError("You have already saved this job.")
        serializer.save(user=self.request.user)

