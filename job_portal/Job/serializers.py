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

    class Meta:
        model = Company
        fields = ['id', 'name', 'description', 'location', 'website', 'average_rating']
        read_only_fields = ['id']

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()  # Assuming related_name='reviews' in CompanyReview
        if reviews.exists():
            return round(sum(review.rating for review in reviews) / reviews.count(), 2)
        return None





class CompanyReviewSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    

    class Meta:
        model = CompanyReview
        fields = ['id', 'company', 'company_name', 'rating', 'review', 'created_at']

