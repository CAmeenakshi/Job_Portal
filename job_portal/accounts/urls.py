from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserSignupViewSet, LogoutView,JobSeekerProfileViewSet, EmployerProfileViewSet

router = DefaultRouter()
router.register('signup', UserSignupViewSet, basename='signup')
router.register('jobseeker-profile', JobSeekerProfileViewSet, basename='jobseeker-profile')
router.register('employer-profile', EmployerProfileViewSet, basename='employer-profile')

urlpatterns = [
    path('', include(router.urls)),
    path('logout/', LogoutView.as_view(), name='logout'),
]
