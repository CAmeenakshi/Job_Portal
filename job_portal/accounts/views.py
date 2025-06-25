from django.shortcuts import render
from rest_framework import viewsets, status,views,permissions,serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from .serializers import UserSignupSerializer,JobSeekerProfileSerializer, EmployerProfileSerializer
from .models import JobSeekerProfile, EmployerProfile
from .models import User
# Create your views here.
# Signup View
class UserSignupViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Logout View
class LogoutView(views.APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"detail": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
        
#JobseekerProfile View
class JobSeekerProfileViewSet(viewsets.ModelViewSet):
    serializer_class = JobSeekerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return only the logged-in user's active (non-deleted) profile
        return JobSeekerProfile.objects.filter(user=self.request.user, is_deleted=False)

    def perform_create(self, serializer):
        if JobSeekerProfile.objects.filter(user=self.request.user, is_deleted=False).exists():
            raise serializers.ValidationError("Profile already exists for this user.")
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        # Soft delete: just set is_deleted = True
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response({"detail": "Profile deleted successfully (soft delete)."},status=status.HTTP_204_NO_CONTENT)

#Employerprofile View

class EmployerProfileViewSet(viewsets.ModelViewSet):
    serializer_class = EmployerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only return profiles that are not soft deleted and belong to current user
        return EmployerProfile.objects.filter(user=self.request.user, is_deleted=False)

    def perform_create(self, serializer):
        if JobSeekerProfile.objects.filter(user=self.request.user, is_deleted=False).exists():
            raise serializers.ValidationError("Profile already exists for this user.")
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        # Perform soft delete by setting is_deleted to True
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response({"detail": "Employer profile deleted successfully (soft delete)."}, status=status.HTTP_204_NO_CONTENT)


