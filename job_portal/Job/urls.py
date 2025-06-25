from rest_framework.routers import DefaultRouter
from .views import JobViewSet,ApplicationViewSet,SavedJobViewSet

router = DefaultRouter()
router.register('jobs', JobViewSet, basename='jobs')
router.register('applications', ApplicationViewSet, basename='application')
router.register('saved-jobs', SavedJobViewSet, basename='saved-jobs')

urlpatterns = router.urls
