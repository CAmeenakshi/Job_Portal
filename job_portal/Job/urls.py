from rest_framework.routers import DefaultRouter
from .views import JobViewSet,ApplicationViewSet,SavedJobViewSet,CompanyViewSet, CompanyReviewViewSet

router = DefaultRouter()
router.register('jobs', JobViewSet, basename='jobs')
router.register('applications', ApplicationViewSet, basename='application')
router.register('saved-jobs', SavedJobViewSet, basename='saved-jobs')
router.register('companies', CompanyViewSet, basename='companies')
router.register('company-reviews', CompanyReviewViewSet, basename='company-reviews')

urlpatterns = router.urls
