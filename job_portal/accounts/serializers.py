from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import RoleEnum
from .models import JobSeekerProfile, EmployerProfile


User = get_user_model()

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ['email','full_name','phone_number','role','password']

    
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        
        # Adding the below line made it work for me.
        instance.is_active = True
        if password is not None:
            # Set password does the hash, so you don't need to call make_password 
            instance.set_password(password)
        instance.save()
        return instance
    
    def validate_role(self,value):
        role_values = [role.value for role in RoleEnum]
        if value not in role_values:
            raise serializers.validationError("Invalid role.")
        return value
    
    

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
