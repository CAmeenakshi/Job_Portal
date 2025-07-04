from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserSignupViewSet, LogoutView,JobSeekerProfileViewSet, EmployerProfileViewSet,ForgotPasswordView, VerifyCodeView, ResetPasswordView

router = DefaultRouter()
router.register('signup', UserSignupViewSet, basename='signup')
router.register('jobseeker-profile', JobSeekerProfileViewSet, basename='jobseeker-profile')
router.register('employer-profile', EmployerProfileViewSet, basename='employer-profile')

urlpatterns = [
    path('', include(router.urls)),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('verify-code/', VerifyCodeView.as_view(), name='verify-code'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
]
