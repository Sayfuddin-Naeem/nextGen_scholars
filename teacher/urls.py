from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DesignationReadOnlyViewset, SpecializationReadOnlyViewset

router = DefaultRouter()
router.register('designation', DesignationReadOnlyViewset, basename='designation')
router.register('specialization', SpecializationReadOnlyViewset, basename='specialization')

urlpatterns = [
    path('', include(router.urls)),
]