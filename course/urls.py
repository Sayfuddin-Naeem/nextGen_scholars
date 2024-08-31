from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet,
    DepartmentReadOnlyViewset,
    CourseEnrollmentViewSet
)

router = DefaultRouter()
router.register('department', DepartmentReadOnlyViewset, basename='department')
router.register('course', CourseViewSet)
router.register('course-enrollment', CourseEnrollmentViewSet, basename='enrollment')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]