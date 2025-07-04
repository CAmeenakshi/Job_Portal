from rest_framework import viewsets, status, views, permissions, serializers
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

from .models import (
    JobSeekerProfile,
    EmployerProfile,
    PasswordResetCode
)
from .serializers import (
    UserSignupSerializer,
    JobSeekerProfileSerializer,
    EmployerProfileSerializer,
    ForgotPasswordSerializer,
    VerifyCodeSerializer,
    ResetPasswordSerializer
)

User = get_user_model()

# USER SIGNUP
# ------------------------------------
class UserSignupViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# USER LOGOUT
# ------------------------------------
class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"detail": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)


# FORGOT PASSWORD - GENERATE CODE
# ------------------------------------
class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                code_obj, _ = PasswordResetCode.objects.get_or_create(user=user)
                code_obj.generate_code()
                # For local testing: return code in response (in real app, send via email)
                return Response({'message': 'Verification code sent.', 'code': code_obj.code})
            except User.DoesNotExist:
                return Response({'error': 'User with this email does not exist.'}, status=404)
        return Response(serializer.errors, status=400)
    
 #RESEND CODE
 # ------------------------------------
class ResendCodeView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                code_obj, created = PasswordResetCode.objects.get_or_create(user=user)
                code_obj.generate_code()  # ✅ Update the code and timestamp
                return Response({
                    'message': 'Verification code resent successfully.',
                    'code': code_obj.code  # ✅ Only show for local testing
                }, status=200)
            except User.DoesNotExist:
                return Response({'error': 'User with this email does not exist.'}, status=404)
        return Response(serializer.errors, status=400)



# VERIFY CODE
# ------------------------------------
class VerifyCodeView(APIView):
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']
            try:
                user = User.objects.get(email=email)
                code_obj = PasswordResetCode.objects.get(user=user, code=code)
                if code_obj.is_expired():
                    code_obj.delete()
                    return Response({'error': 'Code has expired. Please request a new one.'}, status=400)
                return Response({'message': 'Code verified successfully.'})
            except PasswordResetCode.DoesNotExist:
                return Response({'error': 'Invalid code or email.'}, status=400)
        return Response(serializer.errors, status=400)


# RESET PASSWORD
# ------------------------------------
class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']
            new_password = serializer.validated_data['new_password']
            try:
                user = User.objects.get(email=email)
                code_obj = PasswordResetCode.objects.get(user=user, code=code)
                if code_obj.is_expired():
                    code_obj.delete()
                    return Response({'error': 'Code has expired. Please request a new one.'}, status=400)
                user.set_password(new_password)
                user.save()
                code_obj.delete()
                return Response({'message': 'Password has been reset successfully.'})
            except PasswordResetCode.DoesNotExist:
                return Response({'error': 'Invalid code or email.'}, status=400)
        return Response(serializer.errors, status=400)


# JOBSEEKER PROFILE
# ------------------------------------
class JobSeekerProfileViewSet(viewsets.ModelViewSet):
    serializer_class = JobSeekerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return JobSeekerProfile.objects.filter(user=self.request.user, is_deleted=False)

    def perform_create(self, serializer):
        if JobSeekerProfile.objects.filter(user=self.request.user, is_deleted=False).exists():
            raise serializers.ValidationError("Profile already exists for this user.")
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response({"detail": "Profile deleted successfully (soft delete)."}, status=status.HTTP_204_NO_CONTENT)


# EMPLOYER PROFILE
# ------------------------------------
class EmployerProfileViewSet(viewsets.ModelViewSet):
    serializer_class = EmployerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return EmployerProfile.objects.filter(user=self.request.user, is_deleted=False)

    def perform_create(self, serializer):
        if EmployerProfile.objects.filter(user=self.request.user, is_deleted=False).exists():
            raise serializers.ValidationError("Profile already exists for this user.")
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response({"detail": "Employer profile deleted successfully (soft delete)."}, status=status.HTTP_204_NO_CONTENT)
