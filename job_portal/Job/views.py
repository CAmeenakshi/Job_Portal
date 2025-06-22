from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Job
from .serializers import JobSerializer

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
