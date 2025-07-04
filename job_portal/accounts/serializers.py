from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import RoleEnum, JobSeekerProfile, EmployerProfile

User = get_user_model()

# --------------------- USER SIGNUP ------------------------
class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'full_name', 'phone_number', 'role', 'password']

    def validate_role(self, value):
        role_values = [role.value for role in RoleEnum]
        if value not in role_values:
            raise serializers.ValidationError("Invalid role.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        instance.is_active = True  # Optional: sometimes needed for manual activation
        if password:
            instance.set_password(password)
        instance.save()
        return instance

# --------------------- FORGOT PASSWORD FLOW ------------------------

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)

# --------------------- PROFILES ------------------------

class JobSeekerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeekerProfile
        fields = '__all__'
        read_only_fields = ['user']

class EmployerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployerProfile
        fields = '__all__'
        read_only_fields = ['user']
