from rest_framework import serializers
from .models import Job,Application,SavedJob,Company, CompanyReview

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['employer']

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ['user']

class SavedJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedJob
        fields = ['id', 'user', 'job', 'saved_at']
        read_only_fields = ['user', 'saved_at']

class CompanySerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['id', 'name', 'description', 'location', 'website', 'average_rating', 'reviews']

    def get_average_rating(self, obj):
        return round(obj.average_rating(), 2)

    def get_reviews(self, obj):
        return CompanyReviewSerializer(obj.reviews.all(), many=True).data


class CompanyReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyReview
        fields = '__all__'
        read_only_fields = ['jobseeker']
